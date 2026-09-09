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
- **Gap to flag**: the precise relationship diagram among embedded systems / CPS / IoT / real-time embedded systems (Note02 pp. 12, 20–27), and the specific research-topic examples (Note02 pp. 28–34: CPS design challenges, soft real-time timing guarantees, minimizing battery aging, multi-DNN task execution, etc.) were not clearly walked through slide-by-slide in this recording — most of the session's time went to the guest talk (DNN-SAM) instead. Rather than reconstruct those slides' content from the notes alone, refer directly to the original deck (`Lecture_Note02.pdf`).
