1. create ENV 
```bash
python3 -m venv .venv
source .venv/bin/activate 

2. upgarde 

python -m pip install --upgrade pip

3. verify 

which python      # should point inside .venv/bin/python
python --version  # 3.10.x
pip --version     # 26.x or newer

4. Pull the Oracle Database 26ai Free container image

docker pull container-registry.oracle.com/database/free:23.26.1.0

verify docker image : docker images | grep oracle

5. Boot the Oracle 26ai container

docker run -d --name oracle26ai \
  -p 1521:1521 \
  -e ORACLE_PWD=Welcome_123 \
  -v oracle26ai-data:/opt/oracle/oradata \
  container-registry.oracle.com/database/free:23.26.1.0

  6. Confirm the 26ai vector functions actually work, **before** writing any Python. This catches a broken image or a wrong tag in 30 seconds.

docker exec -i oracle26ai sqlplus -S system/Welcome_123@FREEPDB1 <<'SQL'
SET PAGESIZE 0 LINESIZE 200
SELECT VECTOR_DISTANCE(
  TO_VECTOR('[1,2,3]', 3, FLOAT32),
  TO_VECTOR('[4,5,6]', 3, FLOAT32),
  COSINE
) AS cosine_distance FROM dual;
EXIT;
SQL

7. Verify the banner at the same time (sanity check on the build you're running):

docker exec -i oracle26ai sqlplus -S system/Welcome_123@FREEPDB1 <<'SQL'
SET PAGESIZE 0 FEEDBACK OFF
SELECT BANNER_FULL FROM v$version WHERE ROWNUM=1;
EXIT;
SQL

8. Install Python demo dependencies

The dependency list lives in `requirements.txt`

pip3 install path of req.txt

9 . run smoke_test.py thats in scripts 

python3 path of ...smoke_test.py

10. install Ollama for linux

curl -fsSL https://ollama.com/install.sh | sh 

if ZSTD not installed cmd :

 sudo dnf install zstd --disablerepo=google-cloud-sdk

 11. Pulla Ollama 

 ollama pull llama3.1:8b  


 extra info :

 Ollama 0.30.7 = Version of the Ollama software tool itself (the thing that runs LLMs)
llama3.1:8b = The AI model you want to download and run  *****


12.check if ollama is running ?
```bash
ollama run llama3.1:8b "In one sentence, what is RAG?"

13. setup memory for Oracle DB 26i (giving 512Mb )

see if Database is read ?

docker exec oracle26ai /bin/bash -c "while ! sqlplus -S -L sys/Welcome_123@localhost:1521/FREE as sysdba <<< 'SELECT 1; EXIT;' > /dev/null 2>&1; do echo 'Waiting for DB...'; sleep 5; done; echo 'DB is ready'"


check image status ? must show Healthy 

docker ps | grep oracle26ai

then apply the memnory?

docker exec -i oracle26ai sqlplus -S -L sys/Welcome_123@localhost:1521/FREE as sysdba <<'SQL'
ALTER SYSTEM SET vector_memory_size = 512M SCOPE=SPFILE;
EXIT;
SQL

or sometimes even restart to take effect ?

docker restart oracle26ai

till now we have done 2 parts ollama and oracledb 

next is Vector DB creation - install indexes into it [0.23,0,3....etc]

14. the script is in 

/ai-incident-copilot/apps/ai-incident-copilot/scripts/setup_db.sh

execute it how ?

bash /ai-incident-copilot/apps/ai-incident-copilot/scripts/setup_db.sh 

###now insert the data in Vector db thats in oracle DB26 ai

15. file location : /ai-incident-copilot/apps/ai-incident-copilot/src/copilot/db/seed.py

execute how ?

cd /ai-incident-copilot
PYTHONPATH=apps/ai-incident-copilot/src python3 -m copilot.db.seed

Or from the src folder:
cd /ai-incident-copilot/apps/ai-incident-copilot/src
python3 -m copilot.db.seed

(in your case the paths may vary plx check .)


if above fails do 

cd /home/dom/Rahul_wagh_AI_Learn/Project_1/ai-incident-copilot/apps/ai-incident-copilot
cp .env.example .env

and run again 

cd /home/dom/Rahul_wagh_AI_Learn/Project_1/ai-incident-copilot
source .venv/bin/activate
PYTHONPATH=apps/ai-incident-copilot/src python3 -m copilot.db.seed

if again fails do this 

cd /home/dom/Rahul_wagh_AI_Learn/Project_1/ai-incident-copilot
docker exec -i oracle26ai bash -lc "sqlplus -S copilot/Welcome_123@FREEPDB1" < apps/ai-incident-copilot/src/copilot/db/schema.sql

then re run 

PYTHONPATH=apps/ai-incident-copilot/src python3 -m copilot.db.seed

u must see like this output 

##[seed] done — 20 services, 50 incidents, 15 runbooks, links built by category.

16. verify tables in our vector db ?

docker exec -i oracle26ai sqlplus -S copilot/Welcome_123@FREEPDB1 <<'SQL'
SET PAGESIZE 0 FEEDBACK OFF
SELECT 'services         ' || COUNT(*) FROM services;
SELECT 'incidents        ' || COUNT(*) FROM incidents;
SELECT 'runbooks         ' || COUNT(*) FROM runbooks;
SELECT 'incident_runbooks ' || COUNT(*) FROM incident_runbooks;
EXIT;
SQL


output 

ervices         20
incidents        50
runbooks         15
incident_runbooks 107

17.now Langchain which does all the interactions 

/ai-incident-copilot/apps/ai-incident-copilot/src/copilot/agent/tools.py

do u run this too ?

No, you don't run tools.py.

It's a library module that defines the LangChain tools the agent uses. It's imported and called by the agent at query time.

18.next is Fast API 

cd /home/dom/Rahul_wagh_AI_Learn/Project_1/ai-incident-copilot
source .venv/bin/activate
PYTHONPATH=apps/ai-incident-copilot/src uvicorn copilot.api.main:app --host 127.0.0.1 --port 8000

it may show 

   127.0.0.1:33362 - "GET / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:33362 - "GET /favicon.ico HTTP/1.1" 404 Not Found

The 404 errors for / and /favicon.ico are normal — the root path isn't defined, but the API is ready.



troubleshooting if needed:

lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9



19. Stream lit 

cd /home/dom/Rahul_wagh_AI_Learn/Project_1/ai-incident-copilot
source .venv/bin/activate
PYTHONPATH=apps/ai-incident-copilot/src streamlit run apps/ai-incident-copilot/src/copilot/ui/app.py --server.port 8501

trouble shoot:

lsof -i :8501 | grep LISTEN | awk '{print $2}' | xargs kill -9

or 

pkill -f streamlit

it must show that output as : ● API http://127.0.0.1:8000 — healthz: ok when u do localhost:8501


