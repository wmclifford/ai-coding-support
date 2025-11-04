## Context to load

- Read these files first and summarize the constraints you must follow:
  - `Goals.md`
  - `Conventions.md`
  - `System.md`
  - `Tasks/SEC-001.yaml`

## Task

Implement SEC-001 (JWT Authentication) using a 3-pass workflow.

## Constraints

- Edit only these paths:
  - `build.gradle`
  - `src/main/java/**/AuthController.java`
  - `src/main/java/**/AuthRequest.java`
  - `src/main/java/**/AuthResponse.java`
  - `src/main/java/**/AuthService.java`
  - `src/main/java/**/config/**/SecurityConfig.java`
  - `src/main/resources/application*.yml`
  - `src/test/java/**/AuthControllerTest.java`
  - `src/test/java/**/AuthServiceTest.java`
  - `src/test/java/**/QuoteControllerTest.java`
  - `src/test/java/**/config/**/SecurityConfigTest.java`
  - `src/integrationTest/java/**/ApplicationITest.java`
  - `src/integrationTest/java/**/AuthControllerITest.java`
  - `src/integrationTest/java/**/QuoteControllerITest.java`
  - `Tasks/SEC-001.yaml`
- Follow Goals/Conventions/System exactly (reactive WebFlux, RFC 7807, actuator health).
- Unless explicitly requested in task notes, no new dependencies or Gradle plugins; identify if there are any
  required/suggested to complete the task. Allow me to confirm and permit you to use them and update `build.gradle`
  and `gradle/libs.versions.toml` as needed.

## 3-pass Plan

1. Spec

- Ask for clarification from me if a convention is ambiguous.
- List the exact diffs you plan (files/lines), the tests you'll add/modify (if any), and how they satisfy SEC-001.
- Wait for approval.
- Upon approval, create/switch to the branch following the naming convention outlined in the
  Goals/Conventions/System documents. Update the task status to `in_progress` and commit the file.

2. Scaffold

- Apply minimal changes to complete the task requirements.

3. Stabilize

- Make tests pass; tidy config; report test summary and coverage.
- Apply any necessary changes to satisfy this requirement.

## Acceptance Criteria

- `./gradlew check` passes locally.
- `./gradlew jacocoTestReport` passes locally and includes both unit and integration test coverage for existing
  tests; ignore warnings/errors about semantic errors in the JaCoCo test report XML file due to an unregistered URI.
  Line coverage is calculated from `report.counter` where `type="LINE"` using the `missed` and `covered` attributes
  (percentage = (covered / (covered + missed))).
- Follow this process to conclude feature implementation and prepare for review:
  - Update `Tasks/SEC-001.yaml` evidence with commit SHA, test summary, and (if CI is on) the run URL.
  - Update `Tasks/SEC-001.yaml` status to `in_review`.
  - Commit `Tasks/SEC-001.yaml`.

## Output

- Show unified diffs for each file you changed.
- Paste the test run summary and JaCoCo coverage report.
- Call out any QUESTIONS for me if a convention is ambiguous.

