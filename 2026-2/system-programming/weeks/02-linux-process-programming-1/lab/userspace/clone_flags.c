/*
 * clone_flags.c — build your own point on the process/thread spectrum.
 *
 * Linux only (clone(2)). Run in the lab VM.
 *
 * Experiments (all with SIGCHLD as exit signal so waitpid() works):
 *   1. flags = 0            : fork-equivalent — child's write to a global is
 *                             NOT visible to the parent (COW-isolated mm).
 *   2. CLONE_VM             : same write IS visible — shared mm, but the
 *                             child still has its own pid (no CLONE_THREAD):
 *                             two "processes" sharing memory.
 *   3. CLONE_VM only vs
 *      CLONE_VM|CLONE_FILES : child open()s /dev/null; parent tries to
 *                             write() to that fd number. Fails with EBADF
 *                             unless the fd table is shared (CLONE_FILES).
 *
 * CLONE_THREAD is not demonstrated: a CLONE_THREAD task joins the caller's
 * thread group and is no longer a wait()-able child (glibc joins threads via
 * the CLONE_CHILD_CLEARTID futex instead).
 */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>

#define STACK_SIZE (1024 * 1024)

static volatile int counter;
static volatile int fd_from_child = -1;
static volatile pid_t pid_seen_by_child = -1;

/* clone children need their own stack; the kernel does not allocate one. */
static char *alloc_stack(void)
{
	char *p = mmap(NULL, STACK_SIZE, PROT_READ | PROT_WRITE,
		       MAP_PRIVATE | MAP_ANONYMOUS | MAP_STACK, -1, 0);
	if (p == MAP_FAILED) {
		perror("mmap stack");
		exit(1);
	}
	return p + STACK_SIZE;	/* stack grows downwards: pass the top */
}

static int bump_counter(void *arg)
{
	(void)arg;
	pid_seen_by_child = getpid();
	counter += 1000;
	return 0;
}

static int open_devnull(void *arg)
{
	(void)arg;
	pid_seen_by_child = getpid();
	fd_from_child = open("/dev/null", O_WRONLY);
	return 0;
}

static pid_t run_clone(int (*fn)(void *), int flags)
{
	pid_t pid = clone(fn, alloc_stack(), flags | SIGCHLD, NULL);
	if (pid < 0) {
		perror("clone");
		exit(1);
	}
	if (waitpid(pid, NULL, 0) < 0) {
		perror("waitpid");
		exit(1);
	}
	return pid;
}

static void try_parent_write(const char *label)
{
	int fd = fd_from_child;

	if (write(fd, "x", 1) == 1)
		printf("[%s] child opened fd=%d | parent write(fd) -> ok      (shared fd table)\n",
		       label, fd);
	else
		printf("[%s] child opened fd=%d | parent write(fd) -> %s   (separate fd table)\n",
		       label, fd, strerror(errno));
	/* best-effort cleanup; harmless EBADF if table was not shared */
	close(fd);
}

int main(void)
{
	pid_t child;

	printf("parent: pid=%d\n\n", (int)getpid());

	/*
	 * exp1: fork-equivalent — private (COW) mm. The child DID run
	 * bump_counter, but its writes landed in its own page copies:
	 * the parent still sees counter=0 and pid_seen_by_child=-1.
	 */
	counter = 0;
	pid_seen_by_child = -1;
	child = run_clone(bump_counter, 0);
	printf("[exp1 fork-like  ] clone returned pid=%d | parent view: counter=%d, pid_seen_by_child=%d   (isolated mm: child writes invisible)\n",
	       (int)child, counter, (int)pid_seen_by_child);

	/* exp2: CLONE_VM — shared mm, but still a distinct pid (no CLONE_THREAD) */
	counter = 0;
	pid_seen_by_child = -1;
	child = run_clone(bump_counter, CLONE_VM);
	printf("[exp2 CLONE_VM   ] clone returned pid=%d | parent view: counter=%d, pid_seen_by_child=%d   (shared mm: child's getpid()==its own pid)\n\n",
	       (int)child, counter, (int)pid_seen_by_child);

	/*
	 * exp3: fd table sharing. Needs CLONE_VM too, so the parent can read
	 * fd_from_child at all (with a private mm the value would be COW-lost).
	 */
	fd_from_child = -1;
	run_clone(open_devnull, CLONE_VM);
	try_parent_write("exp3 VM only    ");

	fd_from_child = -1;
	run_clone(open_devnull, CLONE_VM | CLONE_FILES);
	try_parent_write("exp3 VM|FILES   ");

	return 0;
}
