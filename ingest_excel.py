import pandas as pd
from db_config import get_connection

import pandas as pd
from db_config import get_connection

def upload_questions_from_excel(file_path, quiz_id=1):
    df = pd.read_excel(file_path)
    print("Excel columns loaded:", df.columns.tolist())
    db = get_connection()
    cursor = db.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO questions (quiz_id, question, option_a, option_b, option_c, option_d, correct_ans)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            quiz_id,
            row['Question'],
            row['Option_A'],
            row['Option_B'],
            row['Option_C'],
            row['Option_D'],
            row['Correct_Ans']
        ))

    db.commit()
    print(f" Questions uploaded to quiz ID {quiz_id}!")


upload_questions_from_excel("template.xlsx", quiz_id=1)

