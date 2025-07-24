
Quiz App (Flask + MySQL)

This is a simple quiz application built using Python (Flask), MySQL, and basic HTML/CSS.  
Users can register, log in, take quizzes, and see their scores.

AWS Deployment 

Architecture Summary:
1. User Browser → accesses Flask app via EC2 public IP.
2. Flask Web App → Hosted on Ubuntu EC2 instance.
3. MySQL Database → Hosted on Amazon RDS (MySQL).
4. Static Files (HTML, CSS, JS) → Served by Flask.

Components Used:
1. Frontend - 	HTML, CSS, JS (Flask templates)
2. Backend	- Python Flask
3. Database - MySQL via AWS RDS
4. Hosting	AWS - EC2 (Ubuntu 24.04, t3.micro)

Manual Setup Steps Summary:
1. Created EC2 instance (Ubuntu, t3.micro)
2. Installed Flask & dependencies via requirements.txt
3. Configured environment variables with .env
4. Created RDS (MySQL) with security groups for EC2 access
5. Imported SQL data into RDS
6. Connected Flask app to RDS
7. Used systemd to run Flask as a service

Security Notes:
1. .env file is used to avoid exposing DB passwords
2. Only necessary ports open (22 for SSH, 80/5000 for HTTP)



<img width="1920" height="1017" alt="Screenshot 2025-07-24 174701" src="https://github.com/user-attachments/assets/53948c14-209d-4d55-8623-c17eb9e8db24" />

<img width="1920" height="1017" alt="Screenshot 2025-07-24 174722" src="https://github.com/user-attachments/assets/ad37f361-a34d-41da-ad14-b31624b6ad2a" />

<img width="1920" height="1002" alt="Screenshot 2025-07-24 174750" src="https://github.com/user-attachments/assets/12770372-34c8-469c-b0dd-f9971e429f82" />

<img width="1920" height="991" alt="Screenshot 2025-07-24 181243" src="https://github.com/user-attachments/assets/99513b7a-f369-4bb4-afcf-49b95edce7d3" />

<img width="1920" height="1017" alt="Screenshot 2025-07-24 181329" src="https://github.com/user-attachments/assets/f0c1bee9-b43b-4a88-806d-3531f48abfde" />

