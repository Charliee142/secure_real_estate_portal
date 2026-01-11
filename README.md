# secure_real_estate_portal
Source code for secure real estate portal built with django

SECURE REAL ESTATE PORTAL
=================================================

Description
-----------
The Secure Real Estate Portal is a full-stack Django web application built to combat
fraud, scams, and lack of trust in online property transactions—especially within
Nigeria and emerging markets.

The platform provides verified property listings, secure digital contracts, encrypted
transactions, and AI-powered fraud detection to ensure safe interactions between
landlords, agents, and renters/buyers.

This project demonstrates how modern web security, AI, and fintech solutions can be
combined to solve real-world problems in the real estate industry.


Problem it Solves
-----------------
Real estate fraud is one of the biggest challenges in Nigeria:
- Fake property listings
- Multiple people paying for the same apartment
- Impersonation of agents/landlords
- No accountability or verification
- Unsafe payment methods

This platform solves these problems by:
- Enforcing verified listings only
- Introducing digital contracts and audit trails
- Using AI to detect suspicious behavior
- Securing payments through trusted gateways
- Providing admin moderation and approval systems


Features
--------
User & Authentication
- Secure authentication using Django-Allauth
- Role-based access (Admin, Agent/Landlord, Buyer/Tenant)
- Email verification and password security

Property Management
- Create, update, and manage property listings
- Admin approval before listings go live
- Image and document uploads
- Availability tracking

Search & Filtering
- Advanced property search
- Filtering by location, price, property type, and status
- Django-filter integration

Booking System
- Property booking with authentication
- Booking status tracking (pending, confirmed, completed)
- Booking history per user

Payments
- Paystack integration for secure booking payments
- Payment verification and transaction logging
- Prevention of duplicate or fake payments

Security & Fraud Prevention
- AI-powered fraud detection for suspicious listings
- User behavior analysis (rapid listings, fake pricing, repeated edits)
- Automated fraud detection cron job
- Encrypted sensitive data
- Secure digital contracts

Admin Dashboard
- Approve or reject listings
- Monitor flagged users and properties
- View analytics and fraud reports

UI & UX
- Bootstrap 5 responsive templates
- Mobile-friendly design
- Clean, professional real estate interface


Tech Stack
----------
Backend:
- Python
- Django
- Django-Allauth
- Django-Filter

Frontend:
- HTML5
- Bootstrap 5
- JavaScript

Database:
- PostgreSQL (Production)
- SQLite (Development)

Payments:
- Paystack API

AI & Automation:
- Python (Scikit-learn / Rule-based ML)
- Django-crontab / Celery for scheduled jobs

Security:
- Django security best practices
- Environment variables for secrets
- CSRF & XSS protection
- Encrypted sensitive fields


Security Measures
-----------------
- Admin verification of all listings
- AI-based fraud detection system
- Secure payment gateway integration
- Encrypted digital contracts
- Environment-based secret key management
- Activity logging and audit trails
- Automated fraud detection cron jobs


Screenshots / Demo
------------------
Screenshots and demo videos will be added here:
- Home Page
- Property Listing Page
- Booking Flow
- Payment Confirmation
- Admin Dashboard
- Fraud Detection Alerts

<img width="960" height="540" alt="1" src="https://github.com/user-attachments/assets/03291411-bc96-41f5-89d3-138278575c88" />
<img width="960" height="540" alt="2" src="https://github.com/user-attachments/assets/ab7abb8a-3c34-4b01-b89a-0fbb8541c8cf" />
<img width="960" height="540" alt="3" src="https://github.com/user-attachments/assets/9da5a473-b49e-4e4b-967f-397a9b48731b" />
<img width="960" height="540" alt="4" src="https://github.com/user-attachments/assets/c09c2c0b-11b3-4f61-8139-ed90d07a44ed" />
<img width="960" height="540" alt="5" src="https://github.com/user-attachments/assets/a0c81b30-c61f-43fb-82dd-51a5287024fe" />
<img width="960" height="540" alt="6" src="https://github.com/user-attachments/assets/f517cf26-3721-4a30-b186-003510617dea" />
<img width="960" height="540" alt="7" src="https://github.com/user-attachments/assets/70917c3a-694c-4b33-aa69-5df5850f5f17" />
<img width="960" height="540" alt="8" src="https://github.com/user-attachments/assets/3d50452f-91f6-4ca2-93f1-8b460cd947b7" />
<img width="960" height="540" alt="9" src="https://github.com/user-attachments/assets/1356925d-ee85-4d52-99fa-f6bc601b0a33" />
<img width="960" height="540" alt="10" src="https://github.com/user-attachments/assets/2c46c3d1-f0e2-44bb-975b-b71feef52aeb" />
<img width="960" height="540" alt="11" src="https://github.com/user-attachments/assets/445301e6-28e5-464c-8d1b-5bf6b5d7f27e" />
<img width="960" height="540" alt="12" src="https://github.com/user-attachments/assets/1f777718-3b05-4fc4-b7c8-4e6b195ebcc1" />
<img width="960" height="540" alt="13" src="https://github.com/user-attachments/assets/a6e1133c-546e-4308-b833-25023062bf12" />
<img width="960" height="540" alt="14" src="https://github.com/user-attachments/assets/fdfa321a-57cc-4958-9390-b3352aed2484" />
<img width="960" height="540" alt="15" src="https://github.com/user-attachments/assets/66dbb51a-a516-4918-8539-5e99af5bea37" />
<img width="960" height="540" alt="16" src="https://github.com/user-attachments/assets/0c5c8db5-7bde-4ef1-8cb0-4841695d1ab9" />
<img width="960" height="540" alt="17" src="https://github.com/user-attachments/assets/8cb58d53-da8f-4bcc-9c76-b832a4806f41" />
<img width="960" height="540" alt="18" src="https://github.com/user-attachments/assets/33747e69-70d9-4162-9e65-dff3f3a45ef7" />
<img width="960" height="540" alt="19" src="https://github.com/user-attachments/assets/47158cdc-e88b-4370-9cdc-2968395231ed" />
<img width="960" height="540" alt="20" src="https://github.com/user-attachments/assets/05c485da-544d-4210-97eb-13c53c1fd123" />
<img width="960" height="540" alt="21" src="https://github.com/user-attachments/assets/09c79c96-16fa-49ba-82b9-89edc712de0a" />
<img width="960" height="540" alt="22" src="https://github.com/user-attachments/assets/e6c85b05-cde7-4f42-86c7-bfb40c7045ff" />
<img width="960" height="540" alt="23" src="https://github.com/user-attachments/assets/e43808db-69a5-4398-9a1d-67eb80c39040" />
<img width="960" height="540" alt="24" src="https://github.com/user-attachments/assets/9c8dcb02-98a8-4091-a1dc-43598a219d06" />
<img width="960" height="540" alt="25" src="https://github.com/user-attachments/assets/68750854-1884-4c77-b269-c9559b15b0b9" />
<img width="960" height="540" alt="26" src="https://github.com/user-attachments/assets/9ffdb6ca-996b-4be7-a176-ccd2ee66e3f2" />
<img width="960" height="540" alt="27" src="https://github.com/user-attachments/assets/493da7c6-2b4e-4986-ab0f-8ed1a25f8ba0" />
<img width="960" height="540" alt="28" src="https://github.com/user-attachments/assets/310d2176-5ea8-410a-9c7a-2ae99e9b175c" />
<img width="960" height="540" alt="29" src="https://github.com/user-attachments/assets/c369cada-33fc-4c0b-ac25-540fdb21e961" />
<img width="960" height="540" alt="30" src="https://github.com/user-attachments/assets/786d0ffc-71a5-487d-95ae-22d460de4343" />
<img width="960" height="540" alt="31" src="https://github.com/user-attachments/assets/c847eff3-2e21-4076-a89c-34b216374aed" />
<img width="960" height="540" alt="32" src="https://github.com/user-attachments/assets/565fbbb5-643e-4483-9ad2-f9d8f788df69" />
<img width="960" height="540" alt="33" src="https://github.com/user-attachments/assets/9ee47b59-e314-4787-860f-7a90accc5545" />
<img width="960" height="540" alt="34" src="https://github.com/user-attachments/assets/1f524102-fe4b-4cc0-aad4-57f4dce02227" />
<img width="960" height="540" alt="35" src="https://github.com/user-attachments/assets/67e8ef1c-68fe-499d-97c3-acd45fb183e8" />

Installation
------------
1. Clone the repository
   git clone https://github.com/Charliee142/secure_real_estate_portal.git
   cd secure_real_estate_portal

2. Create virtual environment
   python -m venv venv
   source venv/bin/activate (Linux/Mac)
   venv\Scripts\activate (Windows)

3. Install dependencies
   pip install -r requirements.txt

4. Setup environment variables
   SECRET_KEY=your_secret_key
   PAYSTACK_SECRET_KEY=your_paystack_key

5. Run migrations
   python manage.py makemigrations
   python manage.py migrate

6. Create superuser
   python manage.py createsuperuser

7. Run development server
   python manage.py runserver


What I Learned
--------------
- How to design secure, scalable Django applications
- Implementing real-world authentication using Django-Allauth
- Integrating payment gateways (Paystack)
- Applying AI concepts to detect fraud patterns
- Protecting applications against real estate scams
- Building admin moderation systems
- Writing production-ready Django code
- Designing systems that solve real Nigerian problems

This project represents my commitment to building secure, impactful solutions using
technology.

Author:
Peter Charles 
Embracing Uniqueness through Tech & Trust



