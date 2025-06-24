# 📝 Django Blog Platform

A powerful blog platform built with Django featuring role-based access. Admins and authors have access to dashboards for content management, while regular users can view published blog posts.

## 🚀 Features

- ✍️ **Author Dashboard** to create, edit, and manage blog posts
- 🛠️ **Admin Dashboard (Superuser)** to manage users, posts, and categories
- 🌐 **Public View** for users to browse blog posts
- 🔐 Role-based access:
  - **Superuser**: Full access (admin panel)
  - **Author**: Custom dashboard to manage own posts
  - **User**: View-only access to published blog content
- 📂 Categories for organizing posts
- 📄 Static pages: About, Contact
- 📱 Responsive frontend with Bootstrap

## 👥 User Roles

| Role        | Dashboard Access      | Permissions                         |
|-------------|------------------------|--------------------------------------|
| Superuser   | Admin dashboard        | Manage users, posts, categories      |
| Author      | Author dashboard       | Create, edit, and delete own posts   |
| User/Guest  | Public blog pages only | View published blog posts            |

## 📁 Project Structure

blog_platform/
- ├── blog/ # Main blog app (views, templates, models)
- ├── post/ # Handles blog post creation/editing
- ├── users/ # Handles authentication and custom user roles
- ├── media/ # Uploaded media (images)
- ├── staticfiles/ # Static assets (CSS/JS/fonts)
- ├── templates/ # Shared HTML templates
- ├── manage.py
- ├── db.sqlite3
- ├── requirements.txt



## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Ranganath099/blog_platform.git
cd blog_platform
2. Set Up Virtual Environment

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
3. Install Dependencies

pip install -r requirements.txt
4. Apply Migrations

python manage.py makemigrations
python manage.py migrate
5. Create Superuser

python manage.py createsuperuser
6. Run Development Server

python manage.py runserver
Access:

Admin Dashboard: http://127.0.0.1:8000/admin/

Blog Homepage: http://127.0.0.1:8000/

✨ To-Do / Future Features
✅ Commenting system

🔄 Pagination and search functionality

📧 Email subscription or contact form backend

🌍 REST API for mobile apps

🖼️ Image uploads for blog posts

⏱️ Blog post scheduling or drafts

🛡 License
This project is licensed under the MIT License.

Made with 💻 by Ranganath B


---

Let me know if you'd like to include screenshots, deployment instructions (like Render, Heroku, or PythonAnywhere), or a `.env` guide.











Tools


