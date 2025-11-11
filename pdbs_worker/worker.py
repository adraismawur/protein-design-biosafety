from sqlite3 import connect
from time import sleep

def main():
  db = connect("pdbs.db")

  while True:
    sleep(1)

    r = db.execute("SELECT id FROM jobs WHERE state = 0 LIMIT 1")

    if r.rowcount == 0:
      continue

    job_id = r.fetchone()[0]

    db.execute("UPDATE jobs SET state = 1 WHERE id = ?", (job_id,))
    db.commit()

    r = db.execute("SELECT * FROM job_params WHERE id = ?", (job_id,))

    job_details = r.fetchone()

    print(job_details)

if __name__ == "__main__":
  main()
