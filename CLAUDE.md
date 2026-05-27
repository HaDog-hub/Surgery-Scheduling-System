# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hospital surgery scheduling system (手術排程系統). A React frontend + Spring Boot backend + standalone Simulated Annealing (SA) algorithm. The SA algorithm runs as an external Java subprocess, not embedded in Spring Boot.

## Commands

### Frontend (root directory)
```bash
npm install          # Install dependencies
npm run dev          # Start Vite dev server (--host enabled)
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend (SERVER/server/)
```bash
mvn spring-boot:run  # Start Spring Boot (requires MySQL on localhost:3306, database: yourdatabase)
```

### Both at once (Windows only)
```bash
start.bat            # Launches both backend and frontend in separate cmd windows
```

### Algorithm — Standalone Execution

**Version 1: ORSM 2025** (legacy, compiled .class only, Java 8)
```bash
cd SERVER/server/ORSM\ 2025
AllInOne.bat         # Uses bundled JDK 1.8, runs SchedulingManager
```

**Version 2: SurgerySchedulerSA** (simple SA)
```bash
cd SERVER/server/SurgerySchedulerSA
javac *.java
java -cp "." Main    # No args; reads from data/in/, writes to data/out/
# Or: runScheduler.bat
```

**Version 3: Surgery-Scheduling-SA_SGDR** (SA + SGDR cosine annealing, currently active in backend)
```bash
cd SERVER/server/Surgery-Scheduling-SA_SGDR
runScheduler.bat     # Compiles *.java then runs: java Main data/in/room.csv data/in/TimeTable.csv configs/SGDR_FOR.csv data/out/newTimeTable.csv
# Or manually:
javac *.java
java Main <room_path> <timetable_path> <sa_config_path> <output_path>
```

### Lint
```bash
npx eslint .         # ESLint with React 18 rules
```

## Architecture

### Three-Tier System

```
React Frontend (Vite + TailwindCSS 4)
    ↓ axios (REST API)
Spring Boot Backend (Java 22, Spring Data JPA)
    ↓ JpaRepository
MySQL Database (localhost:3306/yourdatabase)
    ↓ ProcessBuilder (subprocess)
SA Algorithm (standalone Java, CSV I/O)
```

### Algorithm Invocation Flow

This is the most critical path in the system:

1. **Frontend** (`ORSMButton.jsx`) sends `POST /api/system/algorithm/run` with `closedRoomIds`
2. **AlgorithmController** → **AlgorithmService.runBatchFile()**
3. AlgorithmService exports DB data to CSV files to the active algorithm's input directory:
   - `TimeTable.csv` — all surgeries (excluding pinned/closed rooms)
   - `room.csv` — available operating rooms (written but SA_SGDR derives room info from TimeTable itself)
   - `Arguments4Exec.csv` — time parameters (start time, regular hours, overtime limit, cleaning time)
4. AlgorithmService launches the algorithm's batch file via **ProcessBuilder** (external subprocess)
5. Algorithm reads CSV input → runs optimization → writes results to same output dir:
   - `Guidelines.csv` — human-readable schedule
   - `newTimeTable.csv` — machine-readable assignments
6. AlgorithmService post-processes output:
   - Cleans empty surgeon slots, shifts times forward
   - Re-inserts pinned room schedules (excluded from algorithm)
   - Re-inserts grouped surgeries
   - Parses CSV → updates `Surgery.orderInRoom` and `Surgery.operatingRoom` in DB
   - Recalculates hospital-wide `prioritySequence`

### Three Algorithm Versions

Switching is done by changing 3 constants in `AlgorithmService.java` (lines ~49–57):

```java
// Currently active — Surgery-Scheduling-SA_SGDR:
private static final String BATCH_FILE_PATH = "Surgery-Scheduling-SA_SGDR/runScheduler.bat";
private String ORSM_FILE_PATH = "Surgery-Scheduling-SA_SGDR/data/in";
private String ORSM_GUIDELINES_FILE_PATH = "Surgery-Scheduling-SA_SGDR/data/out";

// To switch to SurgerySchedulerSA (simple SA):
// private static final String BATCH_FILE_PATH = "SurgerySchedulerSA/runScheduler.bat";
// private String ORSM_FILE_PATH = "SurgerySchedulerSA/data/in";
// private String ORSM_GUIDELINES_FILE_PATH = "SurgerySchedulerSA/data/out";

// To switch to ORSM 2025 (legacy):
// private static final String BATCH_FILE_PATH = "ORSM 2025/AllInOne.bat";
// private String ORSM_FILE_PATH = "ORSM 2025";
// private String ORSM_GUIDELINES_FILE_PATH = "ORSM 2025/Guidelines";
```

Also update `time-table.export.path` in `application.properties` to match the active algorithm's input dir.

#### Version 1: ORSM 2025 (Legacy)
- Location: `SERVER/server/ORSM 2025/`
- Entry: `AllInOne.bat` → `SchedulingManager` (compiled .class only, Java 8)
- Bundled JDK 1.8 in `JavaJdk/`
- No source code available — only `.class` files

#### Version 2: SurgerySchedulerSA (Simple SA)
- Location: `SERVER/server/SurgerySchedulerSA/`
- Entry: `runScheduler.bat` → `Main` (no args)
- Input: `data/in/{TimeTable.csv, room.csv, Arguments4Exec.csv}`
- Output: `data/out/{Guidelines.csv, newTimeTable.csv}`
- **SA params**: 500k iterations, T₀=1000, cooling α=0.97 (all hardcoded)
- **Cost**: `5 × overtime + 100 × overlimit` per room
- **Perturbation**: random surgery move between rooms
- **Constraint**: `req=Y` surgeries → special rooms only

#### Version 3: Surgery-Scheduling-SA_SGDR (SA + SGDR Cosine Annealing) — Currently Active
- Location: `SERVER/server/Surgery-Scheduling-SA_SGDR/`
- Entry: `runScheduler.bat` — compiles all `.java` files then runs `Main` with 4 hardcoded args
- Input: `data/in/{TimeTable.csv, Arguments4Exec.csv}` — room data is extracted from TimeTable, not room.csv
- Output: `data/out/{newTimeTable.csv, Guidelines.csv}` — both written to same dir as output arg
- Config files in `configs/` (default: `SGDR_FOR.csv`); to change, edit the `runScheduler.bat` arg
- **Fully configurable** via CSV config: initial solution strategy, cooling strategy, perturbation, termination, cost weights
- **SGDR cooling**: cosine annealing with warm restarts (`T_min + 0.5(T_max−T_min)(1+cos(πt/Ti))`), cycle multiplier, restart decay
- **Initial temperature**: auto-tuned via binary search for target acceptance rate (`TARGET_ACCEPTANCE_RATE`)
- **Cost**: configurable weights `OVERTIME_WEIGHT` and `BALANCE_WEIGHT` for load deviation
- **Termination**: `EVALUATIONS` or `TIME` strategy (set via `TERMINATION_STRATEGY` in config)
- **Also includes**: CP-SAT solver (`CP-SAT.py`), batch experiment scripts (`run_experiments.ps1`), result analysis (`batch_analyzer.py`, `generate_comparison_csv.py`)

### Backend Architecture (Spring Boot)

Standard **Controller → Service → Repository** pattern under `com.backend.project`.

**Controllers** (all under `/api/`):
- `AlgorithmController` — `/api/system/algorithm/` — run algorithm, manage time settings, pin rooms
- `SurgeryController` — `/api/system/surgery/` — CRUD, drag-drop reorder, grouping, CSV upload
- `OperatingRoomController` — `/api/system/operating-room(s)/` — CRUD, toggle status, get surgeries
- `ChiefSurgeonController` — `/api/system/chief-surgeon/` — CRUD
- `DepartmentController` — `/api/system/department/` — CRUD
- `UserController` — `/api/login/`, `/api/system/user/` — auth, password reset, CRUD
- `ScheduleSnapshotController` — `/api/system/schedule/` — daily schedule snapshots

**Key domain concepts:**
- **Surgery grouping**: Multiple surgeries share `groupApplicationIds`; first surgery holds combined estimated time; others get `orderInRoom=null`. All move/delete together.
- **Pinned rooms**: In-memory `ConcurrentHashMap` in AlgorithmService. Pinned rooms are excluded from algorithm input and their schedules are appended to output post-run. **State is lost on backend restart.**
- **Room status**: `0=closed, 1=open`. Closed rooms excluded from algorithm.
- **Room type**: `鉛牆房` = special room that can receive `req=Y` surgeries.
- **orderInRoom**: 1-based integer controlling display order within a room. Reindexed on every add/delete/move.
- **prioritySequence**: Hospital-wide ranking sorted by `estimatedSurgeryTime` descending (longest first). Recalculated after surgery operations.

### Frontend Architecture (React 18)

**Routing** (react-router-dom v7):
```
/ → LoginPageWrapper (login, forgot password, change password)
/system/* → SystemWrapper (fetches user, wraps header + main)
  /system/main    → HomePage (today/tomorrow schedule snapshots)
  /system/mains   → MainGantt (read-only Gantt, admin can toggle edit mode)
  /system/surgery-mgr   → Surgery management CRUD
  /system/shift-mgr     → Shift management + algorithm trigger
  /system/account-mgr   → Account management (admin only, role=3)
  /system/department-mgr → Department management (admin only)
  /system/OR-mgr        → Operating room management (admin only)
```

**Key component interactions:**
- `MainWrapper.jsx` is the central hub: holds shared state (`homeRows`, `shiftRows`, `mainGanttRef`, `initialTimeSettings`, `reservedRooms`), wraps everything in `DragDropContext`
- `MainGantt.jsx` — Gantt chart with drag-drop surgery repositioning. Uses `mainGanttRef` (React ref) to expose state (`hasChanges`, `filteredRows`, `readOnly`) upward to MainWrapper
- `dragEndHandler.jsx` — handles drag-end logic: recalculates times, calls `PUT /surgery/{id}/order-in-room` and `PUT /surgery/{id}/{roomId}`, manages group moves
- `ORSMButton.jsx` — triggers `POST /algorithm/run`, shows loading spinner, clears localStorage on completion
- `ganttData.jsx` — fetches room and surgery data, syncs pinned state with backend
- `timeSettingsWrapper.jsx` — configures algorithm parameters (surgery start time, regular/overtime hours, cleaning time)

**State persistence:**
- Backend DB: surgery positions, room assignments, user data
- localStorage: `shiftRows`, `ganttTimeSettings`, `pinnedRooms`, `reservedClosedRooms`, `home:dnd`
- Ref-based: `mainGanttRef` for cross-component communication without re-renders

**Custom window events** for cross-component communication:
- `ganttDragEnd`, `ganttDataUpdated`, `ganttMainScroll`, `cleaningTimeChange`

**User roles**: 1=surgeon (read-only), 2=manager, 3=admin (full access including algorithm, account/room/department management)

### Time Format Convention

All times are stored as **minutes from midnight** (e.g., `510 = 08:30`). Display conversion happens in `timeUtils.jsx`. Time settings:
- `surgeryStartTime` — daily start (default 510 = 08:30)
- `regularEndTime` — max regular shift duration in minutes
- `overtimeEndTime` — additional overtime allowance
- `cleaningTime` — gap between surgeries (default 45 min)

## API Base URL

Configured in `src/config.js`: use `VITE_API_BASE_URL` for deployed environments; defaults to `http://localhost:8080`.

## Key File Locations

- Frontend entry: `src/main.jsx` → `src/App.jsx`
- Backend entry: `SERVER/server/src/main/java/com/backend/project/ProjectApplication.java`
- Backend config: `SERVER/server/src/main/resources/application.properties`
- Algorithm orchestrator: `SERVER/server/src/main/java/com/backend/project/Service/AlgorithmService.java`
- Algorithm v1 (ORSM): `SERVER/server/ORSM 2025/` (compiled .class only)
- Algorithm v2 (SA): `SERVER/server/SurgerySchedulerSA/Main.java`, `SchedulerSA.java`
- Algorithm v3 (SA+SGDR): `SERVER/server/Surgery-Scheduling-SA_SGDR/Main.java`, `SimulatedAnnealing.java`, `TemperatureManager.java`, `SAConfig.java`
- Algorithm v3 active config: `SERVER/server/Surgery-Scheduling-SA_SGDR/configs/SGDR_FOR.csv`
- Drag-drop logic: `src/components/systemPage/main/Gantt/src/components/DragDrop/dragEndHandler.jsx`
- Algorithm trigger button: `src/components/systemPage/main/Gantt/src/components/Time/ORSMButton.jsx`
