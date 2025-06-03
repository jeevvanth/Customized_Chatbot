import json
import pymysql
from config import hostname,username,password,database


# Step 1: Extract
def extract(json_file):
    with open(json_file) as f:
        return json.load(f)


# Step 2: Transform
def transform(data):
    records = dict()

    for x in data:
        records=data[x]
        print(records)
    return records
    # records=[record for record in data]
    # print(len(records))
    # return records


# Step 3: Load
# def load(data, conn_params):
#     connection = pymysql.connect(**conn_params)
#     cursor = connection.cursor()
#     table_name = "notices"
#     table_name1 = "agencies"
#
#     # Create tables
#     cursor.execute(
#         f"""CREATE TABLE IF NOT EXISTS {table_name} (
#             document_number VARCHAR(20) PRIMARY KEY,
#             title VARCHAR(50),
#             type VARCHAR(50),
#             abstract VARCHAR(50),
#             html_url VARCHAR(50),
#             pdf_url VARCHAR(50),
#             public_inspection_pdf_url VARCHAR(50),
#             publication_date DATE,
#             excerpts VARCHAR(50)
#         )"""
#     )
#
#     cursor.execute(
#         f"""CREATE TABLE IF NOT EXISTS {table_name1} (
#             id INT PRIMARY KEY,
#             document_number VARCHAR(20),
#             raw_name VARCHAR(255),
#             name VARCHAR(255),
#             url VARCHAR(50),
#             json_url VARCHAR(50),
#             parent_id INT,
#             slug VARCHAR(255),
#             FOREIGN KEY (document_number) REFERENCES notices(document_number)
#         )"""
#     )
#
#     # Insert data
#     for record in data:
#         # Insert notice
#         cursor.execute(
#             f"""
#             INSERT INTO {table_name} (document_number, title, type, abstract, html_url, pdf_url,
#                                  public_inspection_pdf_url, publication_date, excerpts)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#             ON DUPLICATE KEY UPDATE
#                 title = VALUES(title),
#                 type = VALUES(type),
#                 abstract = VALUES(abstract),
#                 html_url = VALUES(html_url),
#                 pdf_url = VALUES(pdf_url),
#                 public_inspection_pdf_url = VALUES(public_inspection_pdf_url),
#                 publication_date = VALUES(publication_date),
#                 excerpts = VALUES(excerpts)
#             """,
#             (
#                 record['document_number'],
#                 record['title'],
#                 record['type'],
#                 record['abstract'],
#                 record['html_url'],
#                 record['pdf_url'],
#                 record['public_inspection_pdf_url'],
#                 record['publication_date'],
#                 record.get('excerpts', None)
#             )
#         )
#
#         # Insert agencies
#         for agency in record['agencies']:
#             cursor.execute(
#                 f"""
#                 INSERT INTO {table_name1} (id, document_number, raw_name, name, url, json_url, parent_id, slug)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                 ON DUPLICATE KEY UPDATE
#                     raw_name = VALUES(raw_name),
#                     name = VALUES(name),
#                     url = VALUES(url),
#                     json_url = VALUES(json_url),
#                     parent_id = VALUES(parent_id),
#                     slug = VALUES(slug)
#                 """,
#                 (
#                     agency['id'],
#                     record['document_number'],  # foreign key link
#                     agency['raw_name'],
#                     agency['name'],
#                     agency['url'],
#                     agency['json_url'],
#                     agency['parent_id'],
#                     agency['slug']
#                 )
#             )
#
#     connection.commit()
#     cursor.close()
#     connection.close()



# Pipeline Runner


def load(data, conn_params):
    try:
        # Connect to MySQL
        connection = pymysql.connect(**conn_params)
        cursor = connection.cursor()

        print("Connected to MySQL")

        # Create tables (if they don't exist)
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS notices
                       (
                           document_number
                         VARCHAR(50) PRIMARY KEY,
                           title VARCHAR
                       (
                           255
                       ),
                           type VARCHAR
                       (
                           50
                       ),
                           abstract TEXT,
                           html_url VARCHAR
                       (
                           255
                       ),
                           pdf_url VARCHAR
                       (
                           255
                       ),
                           public_inspection_pdf_url VARCHAR
                       (
                           255
                       ),
                           publication_date DATE,
                           excerpts TEXT
                           )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS agencies
                       (
                           id
                           INT
                           PRIMARY
                           KEY,
                           document_number
                           VARCHAR(50),
                           raw_name VARCHAR
                       (
                           255
                       ),
                           name VARCHAR
                       (
                           255
                       ),
                           url VARCHAR
                       (
                           255
                       ),
                           json_url VARCHAR
                       (
                           255
                       ),
                           parent_id INT,
                           slug VARCHAR
                       (
                           255
                       ),
                           FOREIGN KEY
                       (
                           document_number
                       ) REFERENCES notices
                       (
                           document_number
                       )
                           )
                       """)

        print("✅ Tables created/verified")

        # Insert data
        for record in data:
            try:
                # Insert into 'notices' table
                cursor.execute("""
                               INSERT INTO notices (document_number, title, type, abstract, html_url,
                                                    pdf_url, public_inspection_pdf_url, publication_date, excerpts)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY
                               UPDATE
                                   title =
                               VALUES (title), type =
                               VALUES (type), abstract =
                               VALUES (abstract), html_url =
                               VALUES (html_url), pdf_url =
                               VALUES (pdf_url), public_inspection_pdf_url =
                               VALUES (public_inspection_pdf_url), publication_date =
                               VALUES (publication_date), excerpts =
                               VALUES (excerpts)
                               """, (
                                   record['document_number'],
                                   record['title'],
                                   record['type'],
                                   record['abstract'],
                                   record['html_url'],
                                   record['pdf_url'],
                                   record['public_inspection_pdf_url'],
                                   record['publication_date'],
                                   record.get('excerpts', None)
                               ))

                # Insert into 'agencies' table
                for agency in record['agencies']:
                    cursor.execute("""
                                   INSERT INTO agencies (id, document_number, raw_name, name, url,
                                                         json_url, parent_id, slug)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY
                                   UPDATE
                                       raw_name =
                                   VALUES (raw_name), name =
                                   VALUES (name), url =
                                   VALUES (url), json_url =
                                   VALUES (json_url), parent_id =
                                   VALUES (parent_id), slug =
                                   VALUES (slug)
                                   """, (
                                       agency['id'],
                                       record['document_number'],
                                       agency['raw_name'],
                                       agency['name'],
                                       agency['url'],
                                       agency['json_url'],
                                       agency.get('parent_id'),
                                       agency['slug']
                                   ))

                print(f" Inserted: {record['document_number']}")

            except Exception as e:
                print(f" Failed to insert record {record['document_number']}: {e}")
                connection.rollback()  # Rollback on error

        # Commit changes
        connection.commit()
        print("Data insertion completed!")

    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            connection.close()


def run_pipeline():
    data = extract('response.json')
    cleaned_data = transform(data)

    conn_params = {
        'host': hostname,
        'port':3306,
        'user': username,
        'password':password,
        'database': database,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.Cursor
    }

    load(cleaned_data, conn_params)


if __name__ == "__main__":
    run_pipeline()
