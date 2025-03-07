# Chirper
## The 'Twitter' spinoff everyone needs!
### (or I guess 'X' if you're up to date)

---

## Introduction

Chirper is a social web application that allows users to interact with others on the platform. This project is developed for our Web Development class as our second project of the year. (You can find links to our first project 'task-timer' in our personal GitHubs!)

---

## How it's built

Chirper is built on the Django Framework, using Tailwind CSS for styling to simplify the design process. Additionally, we are using HTMX to give the site a modern, streamlined feel.

### Technologies Used

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Tailwind CSS**: A utility-first CSS framework for rapidly building custom user interfaces.
- **HTMX**: A library that allows you to access modern browser features directly from HTML, making it easier to build interactive web applications.

---

## Features

### User Authentication

- **Signup/Login**: Users can create an account or log in to start using Chirper.
- **Profile Management**: Users can update their profile information, including their profile picture and bio.
- **Toggle Profile Privacy**: Users can switch between public and private profile settings.

### Chirps

- **Create Chirps**: Users can share their thoughts by creating chirps.
- **Like and Reply**: Users can like and reply to chirps from other users.
- **Rich Text Chirps**: Users can use text formatting, images, and videos to enhance their chirps.

### Social Features

- **Follow Users**: Users can follow other users to see their chirps in their feed.
- **Feed**: Users can view chirps from the users they follow in their feed.

### Account Management

- **Delete Account**: Users can delete their account, but their chirps will remain on the platform.

### Enhanced User Experience

- **HTMX Integration**: Enhanced user experience with modern, streamlined interactions.

---

## How to Use

1. **Sign Up/Login**: Create an account or log in to start using Chirper.
2. **Create Chirps**: Share your thoughts by creating chirps.
3. **Interact**: Like and reply to chirps from other users.
4. **Follow Users**: Follow other users to see their chirps in your feed.
5. **Profile Settings**: Toggle your profile privacy and manage your account settings.
6. **Rich Text**: Use rich text formatting to enhance your chirps with bold, underline, images, and videos.

---

## How to Run

### Prerequisites

- Python 3.x
- Django
- Node.js (for Tailwind CSS)

### Steps

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/chirper.git
    cd chirper
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Install Tailwind CSS**:
    ```sh
    npm install
    npx tailwindcss build -o static/css/tailwind.css
    ```

5. **Apply the migrations**:
    ```sh
    python manage.py migrate
    ```

6. **Run the development server**:
    ```sh
    python manage.py runserver
    ```


---

## Tools

### Tailwind Components

[Flowbite Components](https://flowbite.com/#components)
