# CLAUDE.md

This file provides guidance when working with this repository.

## Project Overview

Hospital surgery scheduling system. The app uses a React frontend, a Spring Boot backend, MySQL, and one standalone Java simulated annealing scheduler.

## Commands

### Frontend

```bash
npm install
npm run dev
npm run build
npm run preview
```

### Backend

```bash
cd SERVER/server
mvn spring-boot:run
```

### Both at Once

```bash
start.bat
```

### Algorithm

```bash
cd SERVER/server/SurgerySchedulerSA
javac *.java
java -cp "." Main
# or
runScheduler.bat
```

The scheduler reads CSV files from `data/in/` and writes results to `data/out/`.

## Active Algorithm

The backend currently uses `SurgerySchedulerSA`.

```java
private static final String BATCH_FILE_PATH = "SurgerySchedulerSA/runScheduler.bat";
private String ORSM_FILE_PATH = "SurgerySchedulerSA/data/in";
private String ORSM_GUIDELINES_FILE_PATH = "SurgerySchedulerSA/data/out";
```

The matching properties template values are:

```properties
time-table.export.path=${TIME_TABLE_EXPORT_PATH:SurgerySchedulerSA/data/in}
ORSM.export.path=${ORSM_EXPORT_PATH:SurgerySchedulerSA}
```

## Algorithm Flow

1. Frontend sends `POST /api/system/algorithm/run`.
2. `AlgorithmController` calls `AlgorithmService.runBatchFile()`.
3. `AlgorithmService` exports `TimeTable.csv`, `room.csv`, and `Arguments4Exec.csv` into `SERVER/server/SurgerySchedulerSA/data/in/`.
4. Spring Boot launches `SERVER/server/SurgerySchedulerSA/runScheduler.bat` with `ProcessBuilder`.
5. The scheduler writes `Guidelines.csv` and `newTimeTable.csv` into `SERVER/server/SurgerySchedulerSA/data/out/`.
6. `AlgorithmService` post-processes the output and updates surgery order and operating room assignments in the database.

## Key File Locations

- Frontend entry: `src/main.jsx`, `src/App.jsx`
- Backend entry: `SERVER/server/src/main/java/com/backend/project/ProjectApplication.java`
- Backend config template: `SERVER/server/src/main/resources/application.properties.template`
- Algorithm orchestrator: `SERVER/server/src/main/java/com/backend/project/Service/AlgorithmService.java`
- Active algorithm: `SERVER/server/SurgerySchedulerSA/Main.java`, `SERVER/server/SurgerySchedulerSA/SchedulerSA.java`
- Algorithm trigger button: `src/components/systemPage/main/Gantt/src/components/Time/ORSMButton.jsx`
