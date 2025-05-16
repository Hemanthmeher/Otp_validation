from flask import Flask, render_template, request, session, redirect, url_for, flash
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Email configuration (Use your credentials)
EMAIL_ADDRESS = "hemanthimandi5@gmail.com"
EMAIL_PASSWORD = "ssyy zcpr mkml zbrh"

# Function to send OTP via email
def send_otp(email):
    otp = random.randint(100000, 999999)
    session["otp"] = otp  # Store OTP in session

    # Email message with a personalized touch
    subject = "Your OTP Code for Secure Verification"
    message = f"""
    <html>
    <body>
        <h2 style="color: #333;">Hello,</h2>
        <p>We received a request to verify your email. Please use the OTP below to complete your verification process:</p>
        <h3 style="color: #4285f4; font-size: 24px;">{otp}</h3>
        <p>This OTP is valid for only 10 minutes. Please do not share this code with anyone.</p>
        <br>
        <p>Thank you for using our service! <br> Stay secure,</p>
        <strong>Hemanth Meher/strong>
    </body>
    </html>
    """

    # Creating Email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))  # Sending as HTML email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        if send_otp(email):
            session["email"] = email
            return redirect(url_for("verify"))
        else:
            flash("Failed to send OTP. Please try again.", "error")

    return render_template("index.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        user_otp = request.form["otp"]
        if "otp" in session and int(user_otp) == session["otp"]:
            return redirect(url_for("success"))
        else:
            return redirect(url_for("error"))

    return render_template("verify.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)
