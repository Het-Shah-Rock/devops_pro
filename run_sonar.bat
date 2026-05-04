@echo off
echo =====================================================
echo  QuickCart - SonarQube Analysis Runner
echo =====================================================

echo.
echo [STEP 1] Generating Python Coverage Report for SonarQube...
python -m pytest tests/ --cov=. --cov-report=xml:coverage.xml --junitxml=test-results.xml -q
echo [OK] Coverage report generated: coverage.xml

echo.
echo [STEP 2] Pulling SonarQube Token from environment...
if "%SONAR_TOKEN%"=="" (
    echo [WARN] SONAR_TOKEN not set. Using token from sonar-project.properties
) else (
    echo [OK] SONAR_TOKEN found in environment.
)

echo.
echo [STEP 3] Running SonarScanner analysis...
docker run --rm ^
    -e SONAR_HOST_URL=http://host.docker.internal:9000 ^
    -e SONAR_TOKEN=%SONAR_TOKEN% ^
    -v "%cd%:/usr/src" ^
    sonarsource/sonar-scanner-cli ^
    -Dsonar.projectKey=quickcart-enterprise ^
    -Dsonar.projectName="QuickCart Enterprise" ^
    -Dsonar.projectVersion=1.0 ^
    -Dsonar.sources=. ^
    -Dsonar.inclusions="app.py,database.py,seed.py,pages/**/*.py,tests/**/*.py" ^
    -Dsonar.exclusions="**/__pycache__/**,quickcart.db,*.xml" ^
    -Dsonar.python.coverage.reportPaths=coverage.xml ^
    -Dsonar.python.xunit.reportPath=test-results.xml

echo.
echo [DONE] SonarQube analysis complete!
echo [INFO] View your results at: http://localhost:9000
echo        Project: QuickCart Enterprise
