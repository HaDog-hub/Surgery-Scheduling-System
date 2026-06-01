# Surgery Scheduling System

手術排程管理系統，包含 React 前端、Spring Boot 後端、MySQL 資料庫，以及獨立執行的 Java 模擬退火排程器。

## 技術棧

| 類別 | 技術 |
| --- | --- |
| Frontend | React, Vite, TailwindCSS |
| Backend | Spring Boot, Java 22, Maven |
| Database | MySQL 8 |
| Scheduler | SurgerySchedulerSA |

## 啟動方式

### 後端

```bash
cd SERVER/server
mvn spring-boot:run
```

預設後端網址為 `http://localhost:8080`。

### 前端

```bash
npm install
npm run dev
```

預設前端網址為 `http://localhost:5173`。

### Windows 一鍵啟動

```bash
start.bat
```

## 環境設定

複製後端設定範本：

```bash
cp SERVER/server/src/main/resources/application.properties.template \
   SERVER/server/src/main/resources/application.properties
```

請在 `application.properties` 中設定資料庫帳號密碼：

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/YOUR_DATABASE_NAME?useUnicode=true&characterEncoding=UTF-8&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=Asia/Taipei
spring.datasource.username=YOUR_DB_USERNAME
spring.datasource.password=YOUR_DB_PASSWORD
```

`application.properties` 已被 `.gitignore` 排除，不會提交到 Git。

## 目前使用的演算法

系統目前使用 `SurgerySchedulerSA`：

```text
SERVER/server/SurgerySchedulerSA/
```

後端會將輸入 CSV 匯出到：

```text
SERVER/server/SurgerySchedulerSA/data/in/
```

演算法輸出會寫入：

```text
SERVER/server/SurgerySchedulerSA/data/out/
```

主要設定位於：

- `SERVER/server/src/main/java/com/backend/project/Service/AlgorithmService.java`
- `SERVER/server/src/main/resources/application.properties.template`

## 專案結構

```text
src/                                      React frontend
SERVER/server/src/main/java/com/backend/project/
  Controller/                            REST API
  Service/                               Business logic and scheduler orchestration
  Dao/                                   JPA repositories
  model/                                 Domain models
SERVER/server/SurgerySchedulerSA/        Active scheduling algorithm
docs/screenshots/                        UI screenshots
```

## 功能截圖

![Gantt](docs/screenshots/gantt-main.png)
![Before algorithm](docs/screenshots/before-algorithm.png)
![After algorithm](docs/screenshots/after-algorithm.png)
![Surgery management](docs/screenshots/surgery-management.png)
![Surgery detail](docs/screenshots/surgery-detail.png)
![Account management](docs/screenshots/account-management.png)
![Department management](docs/screenshots/department-management.png)
![Operating room management](docs/screenshots/OR-management.png)
