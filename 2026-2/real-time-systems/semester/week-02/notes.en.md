# Week 02 Lecture Notes — Real-Time Systems (Basic Concepts of Real-Time Systems)

> Source: 2026-09-08 lecture recording STT + slides (`CAS4155_2026Fall_Lecture_Note02.pdf`, in `_private/2026-2/real-time-systems/week-02/`). Instructor: Jinkyu Lee, CAS4155. Also kept in `_private/` for reference: `CAS4155_2026Fall_Lecture_Note01.pdf` (Week 1 admin slides — no recording exists for Week 1 itself, so only the rules re-mentioned in this session are reflected below), `CAS4155_2026Fall_Exercise_A.pdf`, and the guest-talk paper `DNN-SAM_Split-and-Merge_DNN_Execution_for_Real-Time_Object_Detection.pdf`. This is the first course of this term registered in coursebook, so there is no preview chapter (`weeks/`) yet — only a lecture-note digest is produced this time.
>
> **Recording quality caveat**: this recording is quieter and noisier than the other courses' (likely recorded from farther away), so STT quality is uneven throughout. The stretch from t=2641 to t=3150, where the professor is calling on students by name, becomes nearly inaudible, and the STT hallucinated a short loop of repeated words (including, oddly, political figures' names) — that loop was not reproduced verbatim, only the fact that it happened. A few other proper nouns and numbers elsewhere remain uncertain.

## 1. Structure of this session

This (Tuesday) session did not walk through the slide deck in order. Instead it ran: **(1) exercise/logistics reminders → (2) two rounds of student presentations → (3) a guest talk (PhD candidate) → (4) wrap-up**.

1. Exercise A presentation order/rules
2. **Student presentation round 1** — "What is a real-time system" (Catherine) + the professor's supplementary explanation (maps to Note02's basic concepts)
3. A recap of a previous paper (motivating real-time AI resource management) via student presentation, with professor commentary
4. **Student presentation round 2** — three real-world real-time-systems examples (autonomous-driving video analysis, a self-built CNC machine, a 22-motor robot) + Q&A
5. Course-logistics recap (class format, grading, presentation-order rules, attendance, Exercise deadlines)
6. **Guest talk** — PhD candidate Suzan presents "DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection" in full, plus Q&A
7. Wrap-up of Basic Concepts (embedded systems / CPS / real-time-systems relationships, research topics) — maps to Note02's slides

## 2. Exercise A logistics

- Exercise A is a weekly assignment for this 3-credit course (referenced in class with a code that sounded like "2-3-0"; exact meaning should be checked against the slides). The prior submission deadline was the day before (Monday), and presenters walk through their solutions in the Tuesday class.
- **Presentation-order rule**: students who have never presented get top priority. Among students who have already presented, order is first-come-first-served based on Monday-10am sign-up. Priority decreases the more times you've presented — early in the semester, getting a presentation slot is competitive, but by roughly week 10 nearly everyone has presented once, so it becomes easy.
- One student ("Chang-Yi") lost this week's slot for posting too early; another ("Bruno") had his presentation count incorrectly shown as 0 when he had already presented the previous week (corrected in class).
- This session's presenters: **Ying Qing Wang** (referred to in class as "Nancy" — exact spelling should be verified against course materials), presenting on "test screen and timing," and **Bruno**, who presented without narrating much.

## 3. Student presentation — What is a real-time system? (Catherine)

- **Definition**: a real-time system is one whose response must be guaranteed within a specific time limit (looked up online, per the presenter).
- **Why needed**: some systems need critical response times to operate correctly and safely — this connects to the hard/soft real-time distinction covered in class.
  - **Hard real-time**: missing the deadline can cause serious or disastrous real-life consequences.
  - **Soft real-time**: an occasional missed deadline is acceptable, but performance degrades gradually as response time grows.
  - Examples: automatic emergency braking / self-driving cars (failure → injury or death) → hard real-time. Control systems, similarly hard. Telephone systems → soft real-time.
- **Pros**: automates tasks that were impossible or too complex to do immediately; reduces human error via automation requiring precision/consistency; reduces cost by minimizing human intervention; can be customized to specific requirements.
- **Cons**: complex, requires a lot of data and time; expensive to develop; less flexible since safety/correctness must hold; vulnerable to failures/anomalies with potentially serious consequences.
- **General meaning of "real-time"**: data is sent, received, or processed as events occur, rather than stored and handled later. **Real-time does not mean "as fast as possible" — it means a predictable response within a deadline.**
- **Non-CS example**: construction projects — recording cost only after an activity completes is too late for corrections, but reporting cost and progress at the same time (real-time) allows adjustments while still relevant. A nuclear-related example was also mentioned, in the sense that real-time trend-tracking lets you take action to prevent problems/mistakes.
- **Key takeaway**: the system should update at a rate matching what it monitors. What "real-time" means in practice depends on the application's own timescale (a construction project vs. a self-driving car). Real-time information must be available while the event is still in progress.

## 4. Professor's supplementary explanation — basic concepts (maps to Note02)

- **Definition (professor's framing)**: a real-time system's output must be both (1) correct and (2) within a time limit. It operates under a designated time bound (denoted $N_1$ on the slide) and must produce a correct output within it. **This is not about speed** — e.g., a system with a 5-second bound that consistently outputs within 5 seconds still qualifies as real-time.
- **Three-way classification** (per the slide diagram):
  1. **Hard real-time**: missing even a single deadline causes complete, catastrophic system failure. Example: shutdown systems.
  2. **Soft real-time**: missing a response-time deadline does not cause total failure, only degrades user experience.
  3. **Firm real-time**: missing a few deadlines is acceptable — framed in class as "not competing with a perfect system."
- **Scheduler**: how the system behaves depends on the scheduler that orders the task list. The scheduler decides which tasks run and which wait, letting higher-priority tasks take precedence so critical deadlines are met. (Scheduling algorithms themselves are deferred to a later lecture, by category — this session only covers the concept.)
- **Video example**: an airbag-deployment clip slowed down ~100x, illustrating a response that must beat human reaction time (~0.07s) — not that everything needs nanosecond precision, but that things must happen "in time."
- **"Is your PC/laptop a real-time system?"**: student answer was "no." The professor's claim: **"any computer system could be considered a soft real-time system"** — because it ultimately comes down to timing as a function of resources, and the value/benefit you gain decreases as time passes. Example: downloading a file that takes a million years — functionally correct, but no one would call that acceptable → hence treating every computer system as a soft real-time system is, in the professor's own words, "a claim, not necessarily the truth."

## 5. Prior-paper discussion — motivating real-time AI resource management (student recap)

This section is the professor's brief recap of a student presentation on a paper covered in a previous session (exact citation not recoverable from the STT — referred to only as "this article"). **Note: this is a separate, different paper/article from DNN-SAM in section 6.**

- The inspiration for real-time AI comes from biological evidence — humans focus limited cognitive resources (eyes, ears) on what matters most. Current systems, by contrast, process every pixel of an input frame at equal priority, wasting significant resources.
- **Real-time AI resource-management problems** include **saliency estimation** (estimating the importance of different parts of a scene) — e.g., using a depth sensor to focus more attention on certain surfaces/regions.
- Current AI algorithms lack flexibility to reallocate resources, so GPU-level context switching incurs heavy computational overhead, making real-time inference difficult.
- Two factors: **(1) performance isolation** — mixing lower-priority processing with higher-priority frame input appropriately; **(2) performance differentiation** — less important scene regions are processed at lower priority (and thus lower resulting performance), which is accepted as a tradeoff. Compared to a traditional design, this approach adds a priority engine and a VGG network to the architecture.
- The paper's basic argument: two pressures converge — (1) sensors keep advancing, increasing the volume of data systems receive, and (2) market pressure for cost optimization (in a billion-dollar industry, even small optimizations translate to million-dollar savings). Real-time systems are well suited to exactly this pressure environment, since they manage scarce resources by managing system latency.
- Research directions mentioned: **anytime AI** (continually checking whether the current answer is still useful no matter how much time has passed, and dropping it if not — reducing wasted/misused input), and human-like input rectification.

## 6. Student presentations — real-world real-time-systems examples (round 2)

### 6.1 Autonomous-driving video analysis (Shani)

- The vehicle in the video starts slow and progressively optimizes toward its limit speed — related to a very tight deadline.
- Automatic emergency braking must compute time-to-collision, making it a hard real-time system.
- Vibration in the front-mounted camera was mentioned as a real difficulty in synchronizing such sensors, from personal experience.

### 6.2 A self-built CNC machine

- The presenter is building a CNC machine at home (in their bedroom) as a personal project. Large companies typically use a proper CNC controller (e.g., Haas), but a personal project on a limited budget uses cheaper alternatives.
- The controller occasionally freezes — when it should stop exactly at a given point while cutting material, it instead just "cools down" mid-freeze, which can cause serious damage to the workpiece/machine. This illustrates a case that **genuinely needs real-time control** — not fast, but every task must complete before its deadline.

### 6.3 A 22-motor robot

- Updates at roughly 100 Hz, runs on Linux Ubuntu, with JSON-based internal communication.
- With 22 motors, motor-communication bandwidth became a bottleneck that occasionally caused missed deadlines.

### 6.4 The autonomous-driving perceive-plan-control pipeline

- Driving requires three core actions: **(1) perceive** the environment → **(2) plan** what to do → **(3) control** the hardware (brake, turn, accelerate).
- Predictability and meeting every deadline matter — when an obstacle appears, the reaction window is small, and if any single pipeline stage (perceive, plan, or control) takes too long, a collision can result → the presentation's key point: **"it's not just about making the right decision, but making the decision at the right moment."**
- The car carries many sensors running at different frequencies, which must be synchronized into a single common view of the vehicle's state to support correct decisions.
- **Q&A**: a question about predicting collisions between adjacent frames (how relative position changes between consecutive frames of nearby vehicles indicate collision risk) — audio quality made the exact question and answer only partially clear.

## 7. Course-logistics recap (full re-statement)

- **Class format**: Tuesday sessions usually run (1) Exercise presentation/discussion → (2) next Exercise announced → (3) in-class problems → (4) lecture. Thursday is usually lecture-only.
- **Grading**: presentations are worth 10% of the total grade (described as "half of the semester" in relative terms) — you must present at least once during the semester, or you lose that 10%. Priority goes to students who haven't presented yet; early in the semester slots are competitive, but by around week 10 most students have presented once, making slots easy to get (roughly ~10 students total was mentioned — a figure "111" also appears in the raw transcript but its context is unclear).
- **Exercise grading policy**: the TA does not grade strictly — the goal is not to check factual knowledge but to **prompt discussion and thinking**. Most questions are open-ended; the TA checks only whether the answer has sufficient content and then passes it, so most students effectively score 100% — which means **missing an exercise entirely is comparatively very costly**.
- **Announcements**: everything is posted on the LearnUs site — apparently some students had missed this.
- **Presentation sign-up (Exercise B example)**: recommended sign-up by next Monday 10am. Even a two-part problem can be signed up for as a single presentation slot, and presenters may be absent (exact conditions should be verified against the slides).
- **Attendance checks**: around 4:15pm Tuesday and 3:15pm Thursday for this session. No excuses are accepted in general, except for **officially university-approved reasons** (e.g., mandatory reserve-forces training), which require supporting documentation.
- **Allowed absence units**: 9 units total (a Tuesday absence = 2 units, a Thursday absence = 1 unit — missing a whole week costs 3 units). Staying within 9 units incurs no penalty; exceeding it incurs a penalty (referenced as 0.5 out of a 10% block — exact figure should be checked against the slides).
- **Exams**: midterm worth 20%; a figure sounding like "4%" was also mentioned for the final but the context was unclear — verify against the slides. The midterm is scheduled at the same day/time/location as the regular class.
- **Exercise schedule**: usually assigned Tuesday, due the following Monday. This session's new Exercise (uploaded in class) has two problems; one concerns the relationship between time and the exercise itself (see the Exercise file for details).

## 8. Guest talk — DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection

> Presenter: Suzan (PhD candidate, Real-Time Computing Systems Lab, CSE), introduced as joint work with Hanyang University, Sungkyunkwan University, and the University of Michigan. The summary below follows the talk closely and has been cross-checked against the paper PDF (`DNN-SAM_Split-and-Merge_DNN_Execution_for_Real-Time_Object_Detection.pdf`) for terminology.

### 8.1 Problem setting

- Real-time object detection is one of the most challenging and safety-critical functions in autonomous driving (AV). Most AV systems (e.g., Tesla) perform deep-learning-based object detection, with multiple cameras running multiple detection tasks concurrently — typically YOLO-family models on frameworks like PyTorch, TensorFlow, or Darknet, sharing a single computing platform such as NVIDIA Jetson. Providing timely, real-time-guaranteed inference across multiple concurrent DNN tasks under this resource sharing is the central challenge.
- **Two key characteristics**:
  1. Different portions of an input image carry different safety criticality — e.g., the region containing a car and a cyclist matters far more than the background, since missing detection there could be fatal.
  2. This safety-critical region shifts dynamically scene-to-scene — e.g., it moves right as the car turns right.
- Two resulting prerequisites: (1) the high-criticality region needs faster response and higher accuracy, (2) the low-criticality region should be handled within timing requirements while adapting to the moving high-criticality region.
- **Limits of traditional DNN pipelines**: (1) no real-time guarantees at all, (2) uniform treatment of image importance — the full DNN model runs at a single criticality level.
- **Prior work**: dynamic DNN construction (extra layers inserted to adapt to timing constraints, or dynamic multi-exit networks for varying timing constraints) and real-time multi-DNN scheduling frameworks — but these apply equal computation across the whole image and cannot prioritize safety-critical regions. One prior work does differentiate by criticality level but doesn't explicitly handle DNN timing constraints, limiting its real-time guarantees.

### 8.2 DNN-SAM overview

- **DNN-SAM** is a new ML framework realizing dynamic split-and-merge DNN execution and scheduling:
  1. Identify the safety-critical region (the ROI).
  2. Split the original single DNN pipeline into a **mandatory subtask** (takes the cropped image, handles only the safety-critical region) and an **optional subtask** (takes the downscaled full input image, handles the rest within a deadline).
  3. Execute the mandatory subtask first.
  4. Execute the optional subtask.
  5. **Merge** the two subtasks' outputs into the final result.
- **Benefit**: cropping shrinks input size while keeping higher resolution for the safety-critical region → faster response and higher accuracy there. Scheduling the subtasks and adaptively scaling the optional subtask to the ROI size provides the real-time guarantee.
- **Three advantages**:
  1. **Generality**: applies broadly to existing object-detection systems without modifying the core DNN model — since it only rescales/crops the input, it stays applicable even if the underlying model changes.
  2. **Prioritization**: the mandatory subtask is prioritized over the optional one, and its output can be used in advance for other computations (e.g., emergency braking).
  3. **Dynamic adaptation**: captures the time-varying safety-critical region and adaptively selects the optional subtask's scale — even upscaling it beyond the original resolution when there's spare time, to improve accuracy.

### 8.3 Case study

- An emergency-braking experiment on a 1/10-scale self-driving car, with two cameras (front/back) and two detection tasks. The car brakes when a pedestrian is detected within 1.5m on the front camera.
- Metrics compared: perception-and-reaction distance, braking distance, total stopping distance.
- **Baseline**: processes the whole image at once, responds too slowly, misses the deadline, and causes an accident.
- **DNN-SAM**: prioritizes the safety-critical portion, responds faster, brakes within the deadline. Perception-and-reaction distance is reduced **1.9×** versus baseline; DNN-SAM brakes within the safe distance while the baseline exceeds it.

### 8.4 System components (four)

1. **ROI Identification Module**
   - Design principle: since ROI identification sits on the critical path, it must be **fast and predictable**. Instead of a slow DNN-based approach, DNN-SAM uses **sensor fusion** (HD map + LiDAR + camera), determining the ROI based on each object's **time-to-collision (TTC)**.
   - Three steps: (1) **LiDAR segmentation** — segment 3D range data into individual objects via a fast, accurate range-image-based technique; (2) **bounding-box projection** — project 3D boxes into the corresponding 2D camera image; (3) **TTC calculation** — using vehicle distance (LiDAR) and velocity (IMU).
   - Objects under the TTC threshold are selected, and the ROI's location/size is set to include all of them.
2. **Network Split Module**
   - Goal: **seamless and transparent** split-and-merge execution without modifying the DNN model.
   - Generates multiple threads at the framework level for the mandatory/optional subtasks; since the threads share network parameters, overhead is minimized. Also exposes a user API to consume the mandatory subtask's output in advance.
3. **Network Merge Module**
   - Goal: eliminate duplicate detections between the mandatory and optional subtasks for better accuracy.
   - Two issues: (1) objects from both subtasks must be localized in one common global coordinate system; (2) since the mandatory subtask runs on a cropped image, edge objects get detected "cut off."
   - Cut-off objects yield a low **IoU (Intersection over Union)** score, so standard IoU-based duplicate removal fails to recognize them as duplicates. Fix: (1) a coordinate-transformation formula localizing mandatory-subtask detections into the global coordinate system; (2) a new metric that substitutes the union area with the cut-off object's own bounding-box area, letting its score clear the duplicate-detection threshold correctly.
4. **Subtask Scheduler**
   - Goal: schedule multiple DNNs' subtasks and adaptively select the optional subtask's scale, balancing two often-conflicting objectives: (1) schedule mandatory subtasks as early as possible to detect ROI objects quickly, (2) schedule the optional subtask at as large a scale as possible to maximize overall accuracy.
   - Two scheduling algorithms, one per objective:
     - **EDF-Mandatory-First**: maintains two separate queues, statically prioritizing mandatory over optional subtasks (optional only runs when no mandatory subtask is ready); within each queue, priority follows EDF (Earliest Deadline First). The optional subtask's scale is chosen as the largest value that will not delay any future mandatory subtask — favoring scheduling mandatory subtasks as early as possible.
     - **EDF-Slack**: uses a single waiting queue with pure EDF priority (no mandatory/optional distinction), deferring mandatory subtasks as late as their deadline allows to free up more resources for the optional subtask — favoring a larger optional-subtask scale to maximize overall accuracy.
   - **Theoretical result**: a new theorem, based on non-preemptive EDF schedulability analysis, showing that if a certain inequality holds, all mandatory and optional subtasks meet their timing constraints under both algorithms (proof in the paper). Runtime complexity is **O(1)** and **O(N)** respectively (N = number of tasks), incurred at each job release or subtask completion.

### 8.5 Evaluation

- **Setup**: implemented on top of Darknet (no DNN code modification needed), evaluated on NVIDIA Jetson AGX Xavier with YOLOv3, tested on the **KITTI benchmark** (7,000 images), using KITTI's **Velodyne LiDAR point cloud** for ROI identification. Since IMU data isn't provided, a constant forward vehicle speed is assumed.
- **Metrics**: inference latency and inference accuracy (broken into ROI accuracy and overall accuracy), varying the number of tasks from 1 to 6.
- **Latency results**: the baseline meets its FPS requirement only with a single task; with more than one, it fails. Both DNN-SAM variants (EDF, EDF-Slack) meet the FPS requirement across all task counts — as task count grows, more slack becomes available for optional subtasks, and the algorithm adaptively scales them down to keep meeting FPS. EDF-Slack shows the highest average FPS across most task counts, attributed to statically prioritizing mandatory subtasks.
- **Accuracy results**: the baseline's ROI accuracy keeps dropping as task count grows (it must downscale to meet FPS). Both DNN-SAM variants sustain consistently high ROI accuracy regardless of task count — **21.0%** for cars and **29.3%** for pedestrians (interpreted as the improvement figures over baseline — exact basis should be checked against the paper). This reflects the benefit of processing the safety-critical region at its original high resolution. EDF-Slack shows the highest overall accuracy, attributed to securing more resources for optional subtasks while scheduling both efficiently.

### 8.6 Conclusion

- The work targets scenarios (like AV object detection) needing faster response and higher accuracy for safety-critical results, and real-time guarantees for otherwise-fragile DNN tasks. DNN-SAM dynamically splits and merges DNN execution within a real-time framework: a split-and-merge interface transparently decomposing the DNN into two subtasks, plus a lightweight real-time scheduler that prioritizes the mandatory subtask while adaptively scaling the optional one.

### 8.7 Q&A

- **Camera bandwidth/resource-allocation question**: discussion assumed 6 cameras (framed as "6 = 3×2"), each running at 30 FPS over 10 minutes, and the resources needed (e.g., one shared GPU between cameras A and B). A side camera, being less important than the front camera, could run at 15 FPS instead to free up slack. With computing resources genuinely limited (e.g., relative to a Xavier board's capacity), simply combining units doesn't work — a Socratic back-and-forth on where exactly the problem lies:
  - Student answer 1: the two subtasks' inference results could end up different, which is itself a problem.
  - Student answer 2: the baseline treats the whole image the same way even when some regions (e.g., containing a person) matter more.
  - Professor: both are correct, but more fundamentally, **resources (cost, space, communication latency, heat, physical space) are inherently limited** — at autonomous-vehicle scale, even a few cents of cost savings matters.
- **"How does this differ from the previous paper?"**: the earlier paper (section 5) treated object detection/ML tasks as one uniform task with no criticality distinction; DNN-SAM instead distinguishes more-important vs. less-important-but-still-relevant classes within a scene, prioritizing the cropped critical region and using any remaining time to process the rest (downscaled if time is short, full resolution if time allows).
- **Scheduling question**: always prioritizing mandatory tasks makes timing guarantees easier but hurts optional-task responsiveness; alternatively, computing the mandatory tasks' **slack** lets you run optional tasks first whenever there's margin, while still guaranteeing mandatory deadlines (this is the idea behind EDF-Slack).
- **"Isn't ~50% safety-related accuracy too low?"**: the presenter agreed it's low in absolute terms, but defended it by comparison to an ideal, unconstrained reference model — the baseline itself is also very low, so approaching that reference is the intended comparison, while acknowledging the absolute number could still be viewed as too low.
- The professor was explicit that **this course does not teach autonomous-driving system design** — DNN-SAM is presented purely as one example application of real-time scheduling techniques. Questions about whether Tesla uses a similar approach, or whether it's used in home-security products, were answered with "not publicly known, so I don't know."
- Why provide both mandatory-first and select(EDF-Slack) algorithms: choose mandatory-first if the system must prioritize particular critical tasks' responsiveness; choose select if you need balanced average performance across mandatory and optional tasks. Neither is universally better — it depends on the use case.

## 9. Wrap-up — Basic Concepts recap (maps to Note02)

- Covered this session: motivation for real-time systems, their definition, application examples, the relationship among embedded systems / cyber-physical systems (CPS) / real-time systems, and research topics in the field.
- The professor noted that students already had a reasonable intuition for the deadline-centric definition of real-time systems going in.
- **Continued below**: this (2026-09-08) session spent most of its time on the guest talk (DNN-SAM), so the precise relationship among embedded systems / CPS / IoT / real-time embedded systems (Note02 pp. 12, 20–27) and the specific real-time-systems research topics (Note02 pp. 28–34) were not walked through slide-by-slide. That material was covered in a later session (2026-09-10, "Embedded Systems, CPS/IoT & Research Topics") and is written up in **sections 10–12** below.

## 10. [Day 3] "Real-time ≠ fast": revisiting timeliness and predictability

> Source: 2026-09-10 lecture recording (a third session; recap project result document `2026-09-10-real-time-systems-1.json`, titled "Embedded Systems, CPS/IoT & Research Topics"). This session actually covered the Note02 material flagged as missing in section 9 — the embedded-systems/CPS/IoT relationship (pp. 12, 20–27) and the research-topics slides (pp. 28–34); see sections 10–12 below. This recording also has an incompletely-recovered stretch (especially the opening of section 11.1, t≈1200–1800) due to audio quality and context.

- **Opening — CPS examples**: the professor expects the number of CPS research groups/projects to keep growing, citing autonomous vehicles, medical devices (hospitals/ICUs), and small drones as examples.
- **Drone example — how "a little delay" compounds**: if drones need to move immediately but two successive 0.1-second delays occur, the resulting position error can reach 1.5 meters — illustrating why temporal **consistency** matters.
- **Space-time metaphor**: a conveyor belt unboxing items on a timing schedule — when the belt moves defines the system's "space-time."
- **Definition, restated**: a real-time system has a **temporal aspect** as well as a **functional aspect**. Missing the deadline makes an otherwise functionally correct result meaningless — the system won't treat that result as valid.
- **Timeliness as the performance measure**: general-purpose systems are usually measured by speed or average-case performance, but these matter less for real-time systems. The term the professor favors is **timeliness**.
- **System A vs. System B example** (x-axis: number of samples, y-axis: response time):
  - System A: average ~25 (units/sec), maximum 1.5.
  - System B: average ~16, maximum 15–16.
  - From a real-time-systems standpoint, **System B is better** — it's **more predictable** (a student's answer: "time-critical").
  - But the right answer depends on the deadline: with a deadline of 70, System A is bad — it's fine most of the time, but a single miss (e.g., a missed object detection) can be catastrophic. With a deadline of 150, both meet the deadline, so the next criterion becomes average performance, making **System A better**. In other words, **there's no single right answer** — it depends on the system and its deadline.
- **A physical constraint that becomes the deadline**: if the car ahead stops and the gap is 2 meters, at the current speed you have only one second to stop — that physical situation (speed, distance) *is* the **time constraint**.
  - **The loop that implements the deadline**: acquire sensor data → **object detection** (perceive obstacles) → **planning** (including localization and tracking; decide to slow/speed/turn) → **control** (operate the brake pedal, release steering) to actually move the car. If the whole loop must finish within one second, each stage (especially planning) must finish well under that — a **timing constraint imposed by the physical world**.
- **Correcting the misconception: "fast" is not "real-time."** One of this session's key messages: many students come in believing a fast system is (or is what makes) a real-time system — that's wrong.
  - **Metaphor (swimming in a river)**: a person swims in a river with an average depth of 20cm. If the actual depth were exactly 20cm everywhere, drowning would make no sense. But that's just the **average** — the river is 20m long, and some stretch can be far deeper, so the person can still drown.
  - **Lesson**: a real-time system isn't "fast on average" — it has **predictability**. Example: a system from 20 years ago that can guarantee every request finishes within 60 time units has **time predictability**. Conversely, an average response time of 2 units is very fast, but if the worst case is unpredictable, that's not the property a real-time system wants.
  - The professor's favorite phrasing: **"predictable rather than fast."**
- **Hard/Soft/Firm, revisited**: firm real-time has a firm time constraint before the deadline but is not hard real-time — the same three-way classification from sections 3–4, now explained a third time (the professor's own count) with different examples.
- **The "every system is self-predictable" claim, revisited (same argument as section 4)**: if a task on your smartphone took a year to finish, that wouldn't count as "working" → the utility/gain from a result decreases with elapsed time, so every system can be viewed as real-time-related in that sense. The professor adds that, in that sense, we never really have a purely hard/firm real-time system in an absolute sense — while immediately hedging that he's "not sure that makes sense."

## 11. [Day 3] Embedded-systems architecture and the CPS/IoT/real-time-systems relationship (maps to Note02 pp. 12, 20–27)

### 11.1 Embedded-systems examples and constraints (medicine vs. automotive; a Korean research-funding anecdote)

- **A Korean research-funding-history remark (STT uncertain)**: the professor showed a term on a slide (the exact term isn't recoverable from the STT) and said "about 10 years ago, every research proposal in Korea included something like this," giving students a few minutes to think about its meaning. He then asked whether students knew the terms "real-time hypothesis" and "side effect" — but exactly how this connects to the embedded-systems discussion that follows isn't recoverable due to recording quality. **This is plausibly the same thread as the later CPS naming history (see 11.4) — a domestic Korean term that was popular before "CPS" — but that can't be confirmed.**
- **Brainstorming embedded-system examples**: the first example is **medicine** — embedded systems are common in healthcare — followed by a reminder of the embedded-system definition (a device combining a computer, processor, memory, etc. for a dedicated function) and the question "what's the opposite domain?"
- **Leads into automotive/EV** (the exact transition is unclear from the STT): a personal anecdote about a wireless charger — an **EV/mobile wireless-charging episode** where the device kept vibrating without actually charging properly. This leads into the point that people assume mobile devices will just work, but temperature is not irrelevant — automotive embedded systems must withstand large swings, from **Alaska-cold** to **Africa-desert-hot** environments.
- **More automotive-domain constraints**: many vehicles on the road need more power and more charging stations; **water/oceans** are mentioned as another domain for embedded systems; safety requirements for vehicles are mentioned (not just a US-specific requirement).
- **Cost sensitivity (the key point)**: a car company saving even one cent to five dollars per unit matters a great deal — **because production volume is enormous** (e.g., if a controller is produced a million units a day, saving one cent per unit adds up to a huge sum). **Cost really matters.**

### 11.2 General-purpose computer vs. embedded-system architecture

- **General-purpose computer (simplified)**: a computing unit + memory + output + cache.
- **Embedded system (simplified)**: sensor(s) → (with the physical environment in between) → actuator, plus a controller, more sensors, and an **A/D converter** (converting results back to analog to act on the physical world).
- Embedded systems must be designed within constraints — **power, size, weight, and timing** — and be more efficient than general-purpose systems.

### 11.3 The real-time/embedded relationship, and industry/career

- **Most (not all) real-time systems are embedded systems** — why the term "real-time embedded system" is so common.
- However, many of the real-time-system examples covered in class (sections 3, 6) are "not necessarily embedded," since an embedded system is typically **embedded within the operation of some machine**. In other words, **real-time and embedded overlap, but neither is a strict subset of the other.**
- A real-time system is **optimized for more than just functional correctness** — it accounts for more than an initial functional proof, which is what sets it apart from "merely embedded."
- **Industry/career**: the embedded-systems market is growing fast (the professor notes his figures are somewhat outdated). Industries hiring embedded/real-time-systems engineers include: **autonomous systems, telecommunications, consumer electronics, defense and weapons systems, manufacturing software, aerospace, and venture companies.**

### 11.4 Defining cyber-physical systems (CPS) and their naming history

- **Physical** = physical things (cars, robots, etc.). **Cyber** = computing power, control, planning, calculating.
- **Wikipedia definition (quoted directly)**: "CPS is a system of correlated computational elements controlling physical elements." Today, precursor CPS can be found across **aerospace, automotive, chemical processes, civil infrastructure, energy, healthcare, manufacturing, transportation, entertainment, and consumer appliances.**
- CPS is broad enough to cover essentially **every engineering/science field** (materials → physical; mechanical engineering's need for control → cyber) — it's fundamentally an **interdisciplinary** area.
- **Naming history**: the term "CPS" emerged in the US roughly 15+ years ago. Around that time in Korea, a **different term was much more popular** than CPS (possibly connected to the research-funding anecdote in 11.1, though the exact term is not confirmable from the STT). Today in the US, phrases like "I'm a CPS guy" or "my work is CPS research" are common in research proposals.

### 11.5 Defining IoT, and the CPS-vs.-IoT relationship

- **IoT's core idea**: **connection/connectivity**.
- **Wikipedia definition (quoted)**: "IoT is a network of physical things, embedded with electronics, software, and sensors, that enable objects to exchange data with production, operators, and other connected devices" — built on network infrastructure.
- **CPS vs. IoT**: the two overlap heavily and are quite similar, but **IoT focuses on connectivity** while **CPS focuses on the relationship (control) between computing and the physical world** — that's the key difference.
- **A disputed relationship**: CPS researchers often claim IoT is a **subset** of CPS. **The professor (a CPS researcher himself) disagrees** — he sees it as closer to an **intersection** than a strict subset.
- **The real-time-systems community sits closer to CPS** — real-time-systems research is, in the professor's framing, more closely aligned with the CPS community/problem space than with IoT.

## 12. [Day 3] Real-time-systems research topics (maps to Note02 pp. 28–34): time-predictable design and timing analysis

- Presented as the professor's own personal classification: real-time-systems research can be grouped into a few broad topics.
- **Research topic 1 — time-predictable design**:
  - Assumes the standard CS layering (hardware → architecture → programming language → application).
  - Research exists at every layer on "how to achieve time predictability" — e.g., building applications at one layer, or designing an efficient architecture at another.
- **Research topic 2 — timing analysis / analyzability**:
  - Premise: someone designs a system with no regard for timing at all ("here's my system"), and this line of research **analyzes that system after the fact from a timing perspective**.
  - Goal: determine, e.g., "how long does this task take to finish," making the real-time system **analyzable** and its timing visualizable.
- **A concrete example for topic 2 — caches and worst-case analysis**:
  - Question: "is a cache good for average performance?" → well known to be **yes** (memory access is much slower than cache access, so a higher cache hit rate greatly improves average performance).
  - But: "is a cache also good for the **worst case**?" → **a 100% cache hit rate is impossible** — misses will occur in some cases regardless.
  - **The key argument**: from a worst-case standpoint, execution can converge on the path where the cache misses and main memory is accessed anyway — raising the provocative question: "if the worst case always looks like this, might we as well remove the cache entirely, since main memory gets accessed either way?"
  - **Caveat**: the professor is explicit that he's **not** actually arguing to remove all caches — this example is meant only to build intuition that **average-case optimization (caching) and worst-case predictability (time-predictable design) don't necessarily point the same direction**. He notes that real systems/research supporting **time-predictable caches** do exist (deferred to the next Tuesday's class for lack of time).
  - The takeaway framing for this session's research-topics introduction: not just **cache hit rate**, but other topics like **scheduling** can likewise be understood through the tension between "optimizing average performance" and "guaranteeing worst-case predictability."

## 13. [Day 4] Revisiting Exercise B — utility/gain vs. time-delay curves (⚠️ no slide deck this session — recorded from the lecture audio only)

> Source: 2026-09-15 lecture recording (a fourth session; recap project result document `2026-09-15-real-time-systems-1.json`, titled "Exercise B Discussion & Multi-DNN Memory Management (RT-MDM)"; original assumed archived under `_private/2026-2/real-time-systems/week-02/`). **Sections 13 (Exercise B recap), 16 (cache-interference paper discussion), and 18 (RT-MDM presentation) have no corresponding slide deck this term** — the same principle applied to the deck-less "Integer Multiplication" topic in the Algorithm Analysis course's Day 4 (recorded from lecture audio alone). The stretch around t=2776–3251 appears to be cross-talk picked up by the mic while students worked in groups (majors, interests, unrelated to the lecture) and is not reflected in this note.

- This session opened with a review/discussion of Exercise B (drawing the utility/gain vs. time-delay curve for each of hard/firm/soft real-time systems).
- **The "middle" case (corresponds to firm real-time)**: integrity/utility stays constant up to the deadline, then drops immediately to zero the instant the deadline passes — but it never goes negative.
  - **Example — live video analytics**: in real-time object detection, if inference for one frame finishes too late, the result is simply discarded and the system moves on to the next frame. Such a delay is **not treated as a system failure** — presented as the canonical firm-deadline case.
- **Hard real-time, revisited**: finishing within the deadline earns a corresponding utility/monetary gain, but missing the deadline drives achievable utility to **minus infinity, or at least a very large negative number** — e.g., something as bad as a person's death. Hard real-time has many variations, but this is the general case.
- **Firm real-time, revisited**: the deadline should be met, but missing it causes little harm — no gain is achieved, but the result is zero (neither minus infinity nor a large negative number).
- **Soft real-time, revisited**: meeting the deadline is still the ideal, as with hard/firm, but missing it still yields some value depending on how late the result is — a delay very close to the deadline is nearly as good as meeting it, while a very long delay drops to zero just like the firm case.
- **A student question left unresolved**: "How can we actually determine this? For a hard real-time system, what exactly counts as 'good'?" — pointing out that even the hard/firm/soft explanation so far is just a conceptual framework. The professor only said "let's think about this" without giving an explicit answer, then moved on to attendance — **this question was not explicitly answered in this session.**

## 14. [Day 4] Student presentation — tying together real-time systems / embedded systems / CPS / IoT (Rachel)

- Context: a student presentation answering a question left open from earlier sessions — draw a **Venn diagram** of the relationship among real-time systems, embedded systems, CPS, IoT, and other system categories such as biological systems.
- Two presenters: **Rachel (first presenter, a senior in computer science)** and **Agnes (second presenter)**. Only Rachel's content is recoverable from the STT below — **Agnes's presentation is not recoverable due to recording quality in this stretch.**

### 14.1 Rachel's presentation — one diagram built around pairwise intersections

- Her framing: drawing a single Venn diagram for all these systems is hard, because there's heavy overlap while the systems can also be entirely separate. So instead of comparing definitions one by one, she chose to walk through the **intersections** between system pairs.
- Recap of the base definitions (in her own words): **embedded system** = a system built into a larger engineering device to perform a specific function. **CPS** = computing combined with the physical world — it can sense, process, and respond to the physical environment. **Real-time system** = correctness depends not just on what the system does, but on **how it's used** in the physical environment or on the internet.
- **Five intersection examples**:
  1. **Real-time embedded system** = an embedded system with strict timing requirements. Example: a controller embedded in a vehicle — it receives sensor information and must respond quickly; a late response can lead to system failure or serious consequences (tied back to an earlier student-presented example).
  2. **A relatively "pure" real-time system (not clearly overlapping embedded/CPS)**: example — a networked patient monitor. This could also count as CPS since it gathers data from the physical environment. It collects vital signs and other patient data, sends it to the hospital network, and that data is used to assess patient status so the doctor can give timely care.
  3. **Embedded CPS**: built into a larger physical device that interacts with an ecosystem. Example: a smart thermostat — she notes it can also pick up an IoT component (e.g., connected to a phone via another network). It measures temperature from the environment and automatically controls heating/cooling.
  4. **CPS + IoT**: interacts with the physical environment while also interacting with a smart ecosystem over the internet network. Example: smart irrigation — devices store data and send it to a networked actuator; farmers check the information on their mobile devices.
  5. **All four together (embedded + real-time + CPS + IoT)**: the system interacts with the physical world in a highly automated way. Example: **Rachel's own autonomous-car project in Washington** — sensors and cameras interact with the physical environment, and the system had to make decisions under a strict time constraint while relying on other systems over a network ("a bit frustrating, but it was possible").
- **Takeaway**: these systems aren't fully separate. They can be separate in theory, but in real life they tend to be a mixture that overlaps — each category just describes a different aspect.
- Rachel drew this as an **interconnected diagram** rather than plain separate circles (e.g., connected via an internet connection). She then tried to cover IoT's time-sequence model and its evaluation, but ran out of time and only covered the interrelated parts rather than a full comparison — this later stretch of her talk is less well recovered by the STT.

### 14.2 The professor's follow-up discussion — not a subset, and IoT's contested position

- **A claim being pushed back on (STT can't pin down whose claim "his" refers to)**: someone apparently argues that embedded systems belong to a broader category that is entirely contained within CPS (embedded ⊆ CPS). The professor explicitly calls this **the wrong view** — framing it this way, just because CPS is a very broad area, creates a misunderstanding.
- **Counterexamples (presented as part of the same "his" argument, but which actually undercut the subset claim above)**:
  - **A remote control**: an embedded system, but not CPS and not a real-time system.
  - **A real-time OS**: not an embedded system, and not CPS either.
  - **Many systems**: belong to all three of CPS, real-time, and embedded at once (e.g., Rachel's autonomous-car example qualifies).
  - **Optimizing a car's shape**: entirely a CPS problem, but not an embedded-system problem.
  - The professor says he agrees with this **non-subset framing**, calling it "beautiful" — with the caveat that "I'm not saying this is simply a fact, but it's elegant."
- **IoT is the most contested spot**: **the IoT community's view** — IoT is a subset of the broader CPS domain. **The CPS community's view** — IoT is just one example of CPS. The professor says **the CPS-side view is fairer** — while closing with "there's no fixed definition, it's ultimately up to you."
  - **Cross-check**: Day 3's section 11.5 recorded the professor's own position as "IoT isn't a strict subset of CPS, it's closer to an intersection." This session instead uses the phrasing "the CPS community's view (IoT is just one example of CPS) is fairer" — not quite the identical statement. Both agree in rejecting the IoT community's strong subset claim, but the nuance differs, so **rather than flattening them into one, both sessions' actual wording is kept as stated.**

## 15. [Day 4] Course-logistics announcements

- **LearnUs and the Chuseok holiday**: next week is week 4 (September 28). **September 24 (nine days from this session) has no offline class due to the Chuseok holiday and is replaced by a recorded lecture.**
  - The recorded video is available from today until two weeks later (the Monday after next). Watching it within that window counts as attendance for that date; not watching it counts as an absence.
- **Exercise B has been graded**: the TA has already finished grading, so scores can be checked.
  - One student didn't use the template — **always use the designated template.**
  - If a score looks unexpected, re-download the file to see what happened.
  - Further questions go to **the TA by email** — not directly to the professor ("that was my mistake," implying he'd been getting direct emails before). Accept the score as given and don't push further on it.

## 16. [Day 4] Student paper discussion — multi-core cache interference and cache partitioning (⚠️ no slide deck this session — recorded from the lecture audio only; the paper's citation isn't confirmable from STT)

> The paper discussed here is only identified as **published in 2009** — its exact title and authors are not recoverable from the STT. The professor just said to "Google it and download it" (also noting that ACM/IEEE papers are free through the school network), and neither the paper's PDF nor any slides for it are part of this session's materials.

- **Background — revisiting the Day 3 (section 12) question**: "caches are good for average performance, but since a 100% cache hit rate is impossible, are they also good for the **worst case**?" — raised again here in the concrete form of **cache interference in a multi-core setting**.
- **Why caches make time-critical systems hard to build**:
  1. Cache behavior is **unpredictable** from a timing standpoint — cache interference is closely tied to cache misses, and frequent misses make interference time grow unpredictably, making it hard to guarantee **worst-case execution time (WCET)**.
  2. **Cross-core cache interference**: tasks running on different cores can interfere with each other over a (shared) cache, leading to eviction and misses — the core topic of this session.
- **Predictability techniques researchers have proposed (overview)**: cache partitioning (reserving part of the cache for a specific task to prevent interference), worst-case analysis tools for complex architectures, and real-time cache-management techniques (e.g., cache locking).
- **The paper's research method (presented as a general pattern)**: starts without using a real system — derives a **formula** that guarantees timing if some condition holds. A large number of random test cases are generated, and the fraction guaranteed by the formula is checked; the approach is then implemented on real systems for validation. Called "a fairly standard approach for researchers in this area."
- **A worked example in class — why worst-case analysis is hard with multiple tasks**:
  - With a single task, computing the worst-case execution time is no problem. With multiple tasks, the worst case **depends on which other task runs alongside it** — e.g., task A+B might have a worst case of 30ms, while task A+C might be 35ms, varying by combination and hard to compute in general.
  - **Single-core case**: when task 1 runs, its needed data is sometimes cached (fast) and sometimes not (slow) — but this variation **doesn't affect the other task's execution**. Task 2 similarly has its own, independent range of execution times. In a single core, whether a cache access hits or misses can **always be known in advance**.
  - **Multi-core (shared cache), running tasks 1 and 2 concurrently**: task 1 fetches data not in the cache from memory, filling the cache (that data now "belongs" to task 1). Task 2 then also needs data not present in the cache, so it copies its own data in, **evicting task 1's data**. The next time task 1 needs other data, it's no longer there → **tasks 1 and 2 interfere with each other over the cache.** This doesn't happen in a single core — there, we know in advance what will happen, but here we miss the effect of the other task executing concurrently — that's the core problem.
- **A student volunteer's proposed solution (cache partitioning)**:
  - In a single core, tasks write to different regions of the cache, which software can predict in advance. The paper proposes **dividing the cache into partitions and dedicating each partition to a different process**, eliminating inter-task interference — this lets us always predict cache hit/miss in advance, just as in the single-core case.
- **Generalizing to multi-core, worked example**:
  - Suppose there are 4 cache partitions and 4 tasks — naively matching partitions to tasks 1:1 could leave some cores idle. In practice this rarely happens (if it did, you'd just run everything on a single core instead). So we need to consider **how much cache partition each task actually needs** as a separate parameter.
  - Example numbers: task 1 needs 1 unit of partition, task 2 needs 2 units, task 3 needs 2 units, task 4 needs 1 unit (out of 4 total partitions).
  - This paper also determines, via **profiling**, how many partitions each task needs, and schedules based on that. Example: running task 1 (1 unit) and task 2 (2 units) together uses 3 of the 4 partitions, leaving only 1 — not enough to safely accommodate another task (e.g., one needing 2 units), so **that remaining slot is simply left blank (the core stays idle)**.
  - **The key trade-off**: this reduces the cases where interference occurs, but it's still the ideal case — the goal is to keep concurrently running tasks from evicting each other's cached data, achieved by **allocating the right amount of partition**. When that's not possible, **the task is not given the chance to run even if a core is idle** — a design philosophy that prioritizes timing predictability over utilization.
- **Tying back**: the professor revisits this as a concrete instance of "research topic 1 — time-predictable design" from lecture 2 (Note02, Day 3's section 12) — this time showing how to achieve time predictability at the scheduler/task-set level.

## 17. [Day 4] More real-time-systems research-topic examples (networking, battery, ML) — continuing Note02 section 12

> For the stretch around t≈3830–4166, it isn't clear from the STT alone whether the professor or the next presenter (Wenming Zhang) is speaking — the content is summarized below regardless, without asserting who said it.

- **Course-logistics notes (materials/exercises)**: supplement files to be uploaded — lecture material through lecture 7 is already up. **Supplement 1** answers the question "where can you find the state of academic research (specifically, in real-time systems)?" After this week's lecture, supplements 0 and 1 will be covered (lecture 4 is replaced by a recorded lecture, so nothing extra is needed there). The weekly Exercise is due Monday as usual — this week's first question is a recap of this session's lecture, tied to supplement 0 but solvable independently.
- **Framing: timeliness is orthogonal to many CS research areas**: computer science covers a wide range of research areas — operating systems, databases, programming languages, software engineering, and more — but **the real-time property shows up across all of them.** Three additional examples given:
  1. **Networking — software-defined networks (SDN)**: if camera sensors and stream sources are all treated with equal importance and scheduled at the same priority, more important jobs can't be prioritized and deadlines get missed. Designing an SDN lets more important tasks be prioritized — an approach applicable across many applications.
  2. **Physical systems/battery power — drone motor control**: for a physical task that must be controlled periodically (e.g., drone motor control), the amount of power needed at each moment depends on when it's executed. **The total power consumed is the same regardless of the schedule**, but how that power usage is distributed over time affects **battery aging** — "how do we distribute power usage over time to minimize battery aging" is presented as another real-time-systems research topic.
  3. **Machine learning — running under very limited time (mentioned as an example from about eight years ago)**: this third example is the direct lead-in to the RT-MDM presentation in section 18 below.

## 18. [Day 4] Student presentation — RT-MDM: Real-Time Multi-DNN Memory Management on Memory-Constrained MCUs (⚠️ no slide deck this session — recorded from the lecture audio only)

> Presenter: **Wenming Zhang** (Shenzhen University). At the start, the professor told the class it wasn't necessary to fully understand the paper — just to grasp the high-level ideas. Neither a paper PDF nor slides for this presentation are part of this session's materials — the write-up below is reconstructed entirely from the spoken explanation, at the same level of detail as DNN-SAM (section 8).

### 18.1 Problem setup

- MCUs (microcontroller units) are increasingly used in IoT devices for their low cost and low power draw, and since they can gather data very close to the real environment, there's a growing trend toward running various DNN (deep neural network) applications directly on them.
- **Two key challenges**:
  1. **Extremely limited internal memory** — DNN model sizes often exceed it. Prior work has tried to shrink model memory footprint, but MCU memory is still often too small.
  2. **The need for real-time guarantees** — essential as MCUs see more use in time-critical domains. E.g., in autonomous mini-vehicles or drones, failing to guarantee timing can cause collisions; in wearables, if periodic body-signal processing isn't timely, the data can't be trusted.
- **Limits of prior work**: research on guaranteeing real-time DNN execution exists for hardware like GPUs and TPUs, but architectural differences mean it can't be applied directly to MCUs. Work addressing memory limitations, meanwhile, **hasn't considered real-time guarantees for multiple DNN tasks.**
- **RT-MDM's goal**: use **external memory** on MCUs to address **both** the memory limitation and real-time guarantees for multi-DNN tasks at once. Propose a design principle covering both aspects, then build and evaluate a framework based on it.

### 18.2 Background — DNN model segmentation and DMA

- **A common approach to the memory limitation — model segmentation**: store the full model in external memory and split it into segments small enough to fit the internal-memory limit, loading and running them in sequence. Example: with 100KB of internal memory and a 200KB DNN model, the model can't be loaded whole, but split into segments that each fit within 100KB, it becomes runnable — **letting a larger DNN model run with less internal memory.**
- **The catch**: reading segments from external memory adds delay.
- **The fix — DMA (Direct Memory Access)**: a feature on most MCUs that transfers data without going through the CPU, enabling **parallel data transfer and execution**. Example: for a model split into three segments that must be read into internal memory and run in sequence, without DMA the transfer and execution happen sequentially (slow); with DMA, reading and execution overlap, cutting the overall execution time.

### 18.3 The problem with inter-task parallelism

- Given this background, the most intuitive scheduling approach is **segment-level scheduling**, i.e., **inter-task parallelism** — letting different tasks' segment transfers and executions be freely parallelized and preempted.
  - Example: a low-priority task (green) released with no higher-priority task around just runs; but if a higher-priority task (yellow) is released right after, it **preempts** the lower-priority one.
- **Two problems with this approach**:
  1. **Overestimated response time**: response time (when a task actually finishes) is computed as **the task's own worst-case execution time (WCET) plus interference from higher-priority tasks**, and the task is guaranteed schedulable if this stays within its deadline. Allowing inter-task parallelism means multiple higher-priority tasks can keep interfering, making this calculation very complex and forcing a **very pessimistic response-time estimate** — making it very hard to guarantee completion before the deadline. **This response-time-analysis pessimism is exactly the core problem the paper sets out to solve.**
  2. **Memory limitation**: memory stays allocated for a task's data from the moment it's read from external memory until execution finishes, so different tasks' memory-occupied windows can **overlap** — potentially causing memory shortages or forcing data to be reloaded, adding further delay. Continued interference from higher-priority tasks forces lower-priority tasks to hold their data in memory longer, **making the MCU's inherent memory limitation even worse.**

### 18.4 The proposed design — task-level non-preemptive scheduling + segment-group-based memory management

- **The core design — task-level non-preemptive scheduling**: at the task level, **once a task starts, it runs to completion without being preempted by another task** (parallelism is only allowed among a task's own segments). This simplifies timing analysis and improves efficiency — **eliminating the very path by which another task's segments interfere is the core mechanism that reins in the response-time pessimism described in 18.3.**
- **A limitation**: it's ideal when a task's segments achieve maximum parallel utilization, but **memory limits mean maximum parallelism isn't always achievable.** Example: on an MCU with 100KB of internal memory, maximizing parallelism for a model split into three segments would exceed that 100KB limit — so the optimal form in that case is a more limited parallelism.
- **The fix — segment-group-based memory management**: a policy that assigns each task's segments into **groups**. Segments mapped to the same group load and execute sequentially, but **segments mapped to different groups (even across tasks) can run in parallel**, maximizing parallelism and achieving the shortest execution time.
- **Timing analysis**: accounting for the overhead of segmentation and segment-group mapping, response time is computed for each task — this lets the framework **guarantee timing while providing an optimized segment count and group mapping for each task.**
- **The presenter's summary**:
  1. Overcome the MCU's inherent memory limitation by segmenting DNN models and using external memory efficiently via DMA.
  2. Use **task-level non-preemptive scheduling** (no preemption between tasks, parallelism only among ready tasks) to overcome the memory limitation while guaranteeing real-time execution.
  3. Recover the inter-task parallelism lost to the non-preemptive design via the **segment-group mapping policy**.
  4. Provide optimal segmentation and group-mapping strategies via a timing analysis that accounts for the added overhead.

### 18.5 Evaluation

- **Simulation**: scheduling simulations across many tasks — 1,000 random task sets generated per utilization level, for a total of **16,000 task sets** across all utilization levels.
- **Notation**: **IP** = whether internal parallelism is enabled, the second number (N) = whether segmentation is maximized (or reduced to a single segment), and the last number = the segment-group count. **Baseline IP1-1** = the DNN model used with no segmentation at all (unschedulable if the model exceeds internal memory).
- **Results**: the proposed approach (**IP-Optimal**) shows **the highest schedulable ratio across every scenario** — meaning it guarantees real-time execution in more cases than the baseline.
- **Real-system implementation (case study)**: RT-MDM was implemented on an actual **Arduino Nano board**. The practical setup used two DNN tasks — **voice recognition** and **gesture recognition** — assuming 30KB of internal memory. The baseline (IP1-1) can't even run without segmentation, due to the memory limit. **IP-Optimal met both timing and memory constraints without missing a single deadline.**

### 18.6 Conclusion

- To run multiple DNN tasks under an MCU's inherent memory limitation, **RT-MDM** proposes: segmenting DNN models and efficiently using external memory via DMA; **task-level non-preemptive scheduling** (no parallelism between tasks, only among ready tasks, to overcome the memory limitation); recovering inter-task parallelism via **segment-group mapping**; and providing optimal segmentation and group-mapping strategies through an overhead-aware **timing analysis**.

### 18.7 Q&A

- **The professor's comment**: the crux of the problem is that with very low computing power (e.g., a microcontroller whose memory can be under 400KB — a fairly risky level), **even a very lightweight model can't fit entirely in internal memory.** Given a tight timing constraint, how do we handle this efficiently? He frames the essence as: **how do we split the model, and how do we overlap CPU execution with DNN execution to make the most of limited computing power** — closing out the presentation on that note.

## 19. [Day 4] Preview of the next topic — introducing the periodic task model (unfinished, continues Thursday)

- Right after the RT-MDM presentation, the professor opened a new topic (the periodic real-time task model) Socratically, using an **inverted pendulum** example: "how do we keep this inverted pendulum from falling down every time?"
- **Recap of the control loop**: sense the current state via a sensor → compute → actuate the motors. This cycle has to happen "every time."
- **A student-professor exchange narrowing down what "every time" means**:
  - Student answer 1: "nearly the whole time, from when the experiment starts to when it ends" → accepted as correct, with the professor guessing that in this specific case the state-change interval is probably close to the order of **milliseconds** (the exact figure from the paper is unknown).
  - The word "lifetime" also came up — the professor liked the word but said it wasn't quite the exact keyword he wanted.
  - Student answer 2: "divide time into some duration and check at each point whether it's fallen; if those points are mostly fine, call that 'every time'" → assessed as very close.
  - **The concept actually needed turns out to be period**: literally repeating forever is impossible, so what we really have is repeating the process at some specific time period — e.g., every 0.1 seconds.
  - A volunteering student's addition: an analogy to a profiler's two modes, **tracing** and **sampling** — tracing continuously follows the whole process, sampling measures at intervals (a gap). Guaranteeing the pendulum's behavior "every time" would favor the tracing method, they argued, and the professor agreed. He added, though, that what we're actually going to adopt corresponds more to **periodic sampling**, while tracing (given the sense→compute→actuate cycle) is conceptually closer to a half-period.
- **Why periodic control is realistic**: the professor stressed that this periodic modeling isn't an unrealistic theoretical assumption — it comes from **actual control systems from about 50 years ago.** Example: a thermostat (target 23°C, current 20.5°C, checking at some period whether it's over or under target and switching on/off accordingly).
- **Formally introducing the periodic task model**:
  - **Task**: the definition of work that's repeatedly released at some period. **Job**: the single execution instance created at each release.
  - Example (task 1): period 5, relative deadline 4, worst-case execution time (WCET) 2. Jobs are released at times 0, 5, 10, 15, …; each must finish within 4 time units of its release, and since the WCET is 2 units, that 2-unit execution must fit somewhere inside that 4-unit window.
  - Example (task 2): period 7, relative deadline 6 (the exact execution-time figure is unclear from the STT).
  - **The problem setup**: with **only one processor**, control **16** inverted pendulums (= 16 tasks, each with different period/deadline/WCET, since their lengths and weights differ) so that all of them meet their timing on time — stated explicitly as **the base/target model for the entire course.**
- **A hands-on scheduling exercise (scaled down to 4 tasks)**: 4 tasks released at times 0, 4, 8, 12, …, each job (or pair of jobs) constrained to finish within a specified window (e.g., each job of task 1 within 4 time units of its release; two other tasks' job pairs within 5- and 7-unit windows respectively) — students were given 10 minutes to construct a schedule by hand (only partly recoverable, since the exact numbers came from the slide).
- **A priority-based preemptive scheduling example and its failure case**: the blue task gets the highest priority, green the lowest, under preemptive scheduling. At time 0, when all three tasks are ready, they run in priority order (blue → orange → green). But at time 4, the blue task is released again and **preempts** the green task — as a result, **the green task fails to meet its own requirement (2 executions within a 7-time-unit window)** — an example showing priority-based preemptive scheduling can miss a task's deadline.
- **The same priorities applied non-preemptively**: once a task starts, it runs to completion — in this case (checked over the 0–15 window), the resulting schedule looks fine.
- **The professor's closing, unresolved question (deferred to next time)**: "does this non-preemptive schedule stay fine forever, not just over the 0–15 window we observed?" — this question was not answered in this session. **He noted there were many follow-up questions but no time left, and said the remaining slides would continue after Thursday, then ended class.**
- (The session closes noting this topic will be covered in more depth the following Tuesday.)
