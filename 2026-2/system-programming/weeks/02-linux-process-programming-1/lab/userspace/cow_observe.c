/*
 * cow_observe.c — watch copy-on-write happen, in numbers.
 *
 * Linux only (/proc/self/statm, /proc/self/smaps_rollup). Run in the lab VM.
 *
 * Method: touch a 64 MiB anonymous buffer, fork, then in the child snapshot
 *   - RSS from /proc/self/statm,
 *   - Shared_Dirty / Private_Dirty from /proc/self/smaps_rollup
 *     (smaps counts a page as Shared when its mapcount > 1 — i.e. still
 *      COW-shared with the parent — and Private once this task owns it),
 *   - ru_minflt from getrusage() (each COW break is one minor fault)
 * before reading, after reading every page, after writing half the pages,
 * and after writing all pages.
 *
 * Expected: reads cause ~no faults (fork copied the PTEs, read access is
 * allowed); each first write to a page costs exactly one minor fault and
 * moves 4 KiB from Shared_Dirty to Private_Dirty. See README table.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/resource.h>

#define BUF_MIB 64

static long page_size;

static void snapshot(const char *tag)
{
	long size_pages = 0, rss_pages = 0, shared_pages = 0;
	long shared_dirty_kb = -1, private_dirty_kb = -1;
	struct rusage ru;
	char line[256];
	FILE *f;

	f = fopen("/proc/self/statm", "r");
	if (f) {
		if (fscanf(f, "%ld %ld %ld",
			   &size_pages, &rss_pages, &shared_pages) != 3)
			rss_pages = -1;
		fclose(f);
	}

	f = fopen("/proc/self/smaps_rollup", "r");	/* kernel >= 4.14 */
	if (f) {
		while (fgets(line, sizeof(line), f)) {
			sscanf(line, "Shared_Dirty: %ld", &shared_dirty_kb);
			sscanf(line, "Private_Dirty: %ld", &private_dirty_kb);
		}
		fclose(f);
	}

	getrusage(RUSAGE_SELF, &ru);

	printf("%-28s pid=%-6d RSS=%4ld MiB  Shared_Dirty=%6ld kB  "
	       "Private_Dirty=%6ld kB  minflt=%ld\n",
	       tag, (int)getpid(),
	       rss_pages * page_size / (1024 * 1024),
	       shared_dirty_kb, private_dirty_kb, ru.ru_minflt);
	/*
	 * Flush now: if stdout is redirected to a file/pipe it is fully
	 * buffered, and the child's _exit(0) would silently drop its lines.
	 * Flushing here (incl. right before fork) also avoids the parent's
	 * buffered output being duplicated into the child.
	 */
	fflush(stdout);
}

int main(void)
{
	size_t len, i;
	char *buf;
	pid_t pid;

	page_size = sysconf(_SC_PAGESIZE);
	len = (size_t)BUF_MIB * 1024 * 1024;

	buf = malloc(len);
	if (!buf) {
		perror("malloc");
		return 1;
	}
	memset(buf, 0xAA, len);		/* touch every page: now Private_Dirty */
	snapshot("parent before fork");

	pid = fork();
	if (pid < 0) {
		perror("fork");
		return 1;
	}

	if (pid == 0) {
		volatile long sum = 0;

		snapshot("child  after fork");

		for (i = 0; i < len; i += (size_t)page_size)
			sum += buf[i];	/* reads: no COW faults expected */
		(void)sum;
		snapshot("child  after read all");

		for (i = 0; i < len / 2; i += (size_t)page_size)
			buf[i] = 0x55;	/* one COW fault per page */
		snapshot("child  after write half");

		for (i = len / 2; i < len; i += (size_t)page_size)
			buf[i] = 0x55;
		snapshot("child  after write all");
		_exit(0);
	}

	waitpid(pid, NULL, 0);
	snapshot("parent after child exit");	/* mapcount back to 1 → Private */

	free(buf);
	return 0;
}
