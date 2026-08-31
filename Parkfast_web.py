from flask import Flask, render_template_string, request, redirect, url_for, flash, session , jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from random import randint
from flask_mail import Mail, Message
from email.mime.text import MIMEText
import random
import smtplib
import mysql.connector
import serial
import threading
from email.mime.text import MIMEText

app = Flask(__name__)
mail = Mail(app)

app.secret_key = "your_secret_key"

# MySQL Config
db_config = {
    "host": "localhost",
    "user": "Rudran",
    "password": "Rudran@2005",
    "database": "sps_project"
}


# Email sender
def send_otp_email(recipient, otp):
    sender = "rudran.development@gmail.com"
    password = "dyfl dcrv fcrw nerb"
    subject = "🔐 OTP for Password Reset"

    # HTML Body
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Your OTP for ParkFast</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #f4f4f5;
                font-family: Arial, sans-serif;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 30px auto;
                background: #ffffff;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }}
            .header {{
                background-color: #0f172a;
                text-align: center;
                padding: 30px;
            }}
            .header img {{
                width: 120px;
                margin-bottom: 10px;
            }}
            .header h1 {{
                color: #ffffff;
                font-size: 24px;
                margin: 0;
            }}
            .content {{
                padding: 30px;
                text-align: center;
            }}
            .content h2 {{
                color: #0f172a;
                font-size: 22px;
                margin-bottom: 15px;
            }}
            .content p {{
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 20px;
            }}
            .otp-box {{
                display: inline-block;
                padding: 16px 32px;
                background-color: #e0e7ff;
                color: #1e40af;
                font-size: 26px;
                font-weight: bold;
                border-radius: 8px;
                letter-spacing: 2px;
                margin: 20px auto;
            }}
            .footer {{
                background-color: #f1f5f9;
                padding: 20px;
                text-align: center;
                font-size: 14px;
                color: #6b7280;
            }}
            .footer a {{
                color: #0f172a;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://www.shutterstock.com/image-vector/vector-icon-parking-cars-sign-600nw-2490009635.jpg" alt="ParkFast Logo">
                <h1>Password Reset OTP</h1>
            </div>
            <div class="content">
                <h2>🔐 Your One-Time Password</h2>
                <p>We received a request to reset your password. Use the OTP below to proceed:</p>
                <div class="otp-box">{otp}</div>
                <p>This OTP is valid for a limited time. Please do not share it with anyone.</p>
                <p>If you didn’t make this request, just ignore this email — your account is safe.</p>
            </div>
            <div class="footer">
                Need help? Email us at 
                <a href="mailto:support@parkfast.in">support@parkfast.in</a><br><br>
                &copy; 2025 ParkFast · All rights reserved
            </div>
        </div>
    </body>
    </html>
    """

    message = MIMEText(html, "html")
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(message)
        return True
    except Exception as e:
        print("Email sending error:", e)
        return False

# FRONTEND CODE HTML TAILWINDCSS 
            
signup_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up | ParkFast</title>
    <script src="https://cdn.tailwindcss.com"></script>

    <style>
        body {
            background-color: #202427;  /* Background color set to #202427 */ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        }

        .card {
            background-color: #ffffff;
            border-radius: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }

        .card:hover {
            box-shadow: 0 6px 25px rgba(0, 0, 0, 0.12);
        }

        .footer-links {
            color: #0078d4;
            text-decoration: none;
        }

        .footer-links:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body class="flex justify-center items-center min-h-screen">

    <div class="card w-full max-w-md p-8">
<!-- Logo -->
<div class="flex justify-center mb-6">
    <img src="{{ url_for('static', filename='images/login-logo.png') }}" 
         alt="ParkFast Logo" 
         class="h-24 md:h-28 object-cover rounded-2xl shadow-lg bg-transparent" />
</div>


        <!-- Heading -->
        <h2 class="text-3xl font-semibold text-center text-gray-800 mb-8">Create Your ParkFast Account</h2>

        <!-- Flash Message -->
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="bg-green-100 text-green-800 p-3 rounded-lg mb-4 text-center">
                    {{ messages[0] }}
                </div>
            {% endif %}
        {% endwith %}

        <!-- Sign Up Form -->
        <form method="POST" action="/signup" class="space-y-5">
            <div>
                <input name="name" type="text" placeholder="Full Name" required
                    class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
            </div>

            <div>
                <input name="email" type="email" placeholder="Email Address" required
                    class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
            </div>

            <div>
                <input name="password" type="password" placeholder="Create a Password" required
                    class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
            </div>

            <button type="submit"
                class="w-full py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition duration-300">
                Sign Up
            </button>
            
        </form>

        <div class="text-center mt-6 text-sm text-gray-500">
            <p>By signing up, you agree to our 
                <a href="#" class="footer-links">Terms of Service</a> and 
                <a href="#" class="footer-links">Privacy Policy</a>.
            </p>
        </div>

        <div class="text-center mt-4 text-sm text-gray-500">
            <p>Already have an account? 
                <a href="/login" class="footer-links">Sign In</a>
            </p>
        </div>

    </div>

</body>
</html>



"""
# ================= LIVE PARKING SYSTEM =================

COM_PORT = "COM7"
BAUD = 9600

def parking_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rudran@2005",
        database="parkfast"
    )

# UPDATE SLOT STATUS
def update_slot(slot_id, status):

    conn = parking_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE slot_status SET status=%s WHERE slot_id=%s",
        (status, slot_id)
    )

    conn.commit()
    conn.close()

# READ ARDUINO DATA
def read_arduino():

    try:
        arduino = serial.Serial(COM_PORT, BAUD, timeout=1)
        print("Arduino Connected Successfully")

    except Exception as e:
        print("Arduino Error:", e)
        return

    while True:

        data = arduino.readline().decode().strip()

        if data:

            print("Received:", data)

            if data == "SLOT1:PARKED":
                update_slot(1, "PARKED")

            elif data == "SLOT1:AVAILABLE":
                update_slot(1, "AVAILABLE")

            elif data == "SLOT2:PARKED":
                update_slot(2, "PARKED")

            elif data == "SLOT2:AVAILABLE":
                update_slot(2, "AVAILABLE")

# START ARDUINO THREAD
threading.Thread(target=read_arduino, daemon=True).start()

# LIVE PARKING PAGE
live_parking_page = """

<!DOCTYPE html>
<html>
<head>

<title>Live Parking</title>

<script src="https://cdn.tailwindcss.com"></script>

<style>

body{
    background:#f3f4f6;
}

.slot{
    width:220px;
    height:140px;
}

</style>

</head>

<body class="flex flex-col items-center justify-center min-h-screen">

<h1 class="text-4xl font-bold mb-10 text-gray-800">
🚗 Live Parking Updates
</h1>

<div class="flex gap-10">

    <div id="slot1"
         class="slot bg-green-500 rounded-2xl shadow-xl flex items-center justify-center text-white text-2xl font-bold">
         Available
    </div>

    <div id="slot2"
         class="slot bg-green-500 rounded-2xl shadow-xl flex items-center justify-center text-white text-2xl font-bold">
         Available
    </div>

</div>

<script>

async function loadStatus(){

    const response = await fetch("/api/live_slots");

    const data = await response.json();

    data.forEach(slot => {

        let box = document.getElementById("slot" + slot.slot_id);

        if(slot.status === "PARKED"){

            box.className =
            "slot bg-red-500 rounded-2xl shadow-xl flex items-center justify-center text-white text-2xl font-bold";

            box.innerText = "Parked";

        }else{

            box.className =
            "slot bg-green-500 rounded-2xl shadow-xl flex items-center justify-center text-white text-2xl font-bold";

            box.innerText = "Available";
        }

    });

}

setInterval(loadStatus,1000);

loadStatus();

</script>

</body>
</html>

"""

# LIVE PARKING ROUTE
@app.route("/live_parking")
def live_parking():
    return render_template_string(live_parking_page)

# LIVE SLOT API
@app.route("/api/live_slots")
def api_live_slots():

    conn = parking_db()

    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT * FROM slot_status ORDER BY slot_id"
    )

    data = cur.fetchall()

    conn.close()

    return jsonify(data)

# ================= END LIVE PARKING SYSTEM =================
login_page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Login | ParkFast</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {
      background-color: #202427; /* Deep background color */
      font-family: 'Poppins', sans-serif;
    }

    .card {
      background: #ffffff;
      border-radius: 1.5rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
      transition: all 0.3s ease;
    }
    .card:hover {
      box-shadow: 0 6px 25px rgba(0, 0, 0, 0.12);
    }

    /* Ensure image scales properly and fits */
    .logo {
      width: auto;
      max-width: 100%;
      height: auto;
      max-height: 100px; /* Adjust this as per your requirement */
    }
  </style>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
</head>

<body class="flex items-center justify-center min-h-screen">

  <div class="card w-full max-w-md p-10">
    <!-- Logo -->
    <div class="flex justify-center mb-6">
      <img src="{{ url_for('static', filename='images/login-logo.png') }}" 
           alt="ParkFast Logo" 
           class="logo object-cover rounded-2xl shadow-lg bg-transparent" />
    </div>

    <!-- Heading -->
    <h2 class="text-2xl font-semibold text-center text-gray-800 mb-8">Sign in to ParkFast</h2>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="bg-green-100 text-green-800 text-sm p-3 rounded-lg mb-6 text-center">
          {{ messages[0] }}
        </div>
      {% endif %}
    {% endwith %}

    <!-- Form -->
    <form method="POST" action="/login" class="space-y-5">
      
      <div>
        <label class="text-sm text-gray-600">Email Address</label>
        <input name="email" type="email" placeholder="you@example.com" required
          class="w-full px-4 py-3 mt-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
      </div>

      <div>
        <label class="text-sm text-gray-600">Password</label>
        <input name="password" type="password" placeholder="Password" required
          class="w-full px-4 py-3 mt-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
      </div>

      <button type="submit"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition duration-300">
        Sign In
      </button>

    </form>
    <div class="flex items-center my-6">
    <hr class="flex-grow border-t border-gray-300">
    <span class="px-4 text-gray-400">or</span>
    <hr class="flex-grow border-t border-gray-300">
</div>

<!-- Google Sign In Button -->
<div class="text-center">
    <a href="#"
       class="w-full inline-flex items-center justify-center py-3 px-4 border border-gray-300 rounded-lg shadow-sm bg-white hover:bg-gray-100 transition">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/2048px-Google_%22G%22_logo.svg.png" 
             alt="Google Logo" class="w-5 h-5 mr-3">
        <span class="text-sm font-medium text-gray-700">Continue with Google</span>
    </a>
</div>


    <!-- Links -->
    <div class="text-center text-sm text-gray-500 mt-6 space-y-2">
      <p>
        <a href="/forgot" class="hover:underline text-blue-600">Forgot Password?</a>
      </p>
      <p>
        Don't have an account?
        <a href="/signup" class="text-blue-600 hover:underline">Sign Up</a>
      </p>
    </div>

  </div>

</body>
</html>


"""

dashboard_page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dashboard | ParkFast</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
  <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
  <style>
    html {
      scroll-behavior: smooth;
    }
    .custom-font {
      font-family: 'Agency FB', sans-serif;
      font-weight: bold;
    }
  </style>

  <style>
@keyframes fadeIn {
  0% { opacity: 0; transform: scale(0.95); }
  100% { opacity: 1; transform: scale(1); }
}
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
</style>

  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap" rel="stylesheet">
</head>
<body class="flex h-screen bg-gradient-to-br from-gray-50 to-gray-200 overflow-hidden font-sans">
<!-- Welcome Popup -->
<div id="welcomePopup" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50 hidden">
  <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full relative text-center animate-fade-in">
    <button onclick="closePopup()" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700 text-2xl font-bold">&times;</button>
    <img src="{{ url_for('static', filename='images/login-logo.png') }}" alt="ParkFast Logo" class="h-16 mx-auto mb-4">
    <h2 class="text-2xl font-extrabold text-gray-800 mb-4">Welcome to ParkFast! 🚗</h2>
    <p class="text-gray-600 mb-4">Your smart parking assistant is here. Find parking faster, pay securely, and drive stress-free!</p>
    <button onclick="closePopup()" class="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-full transition-all duration-300">
      Let's Go
    </button>
  </div>
</div>

  <!-- Sidebar -->
  <aside class="w-64 bg-[#111827] flex flex-col text-white shadow-xl transition-all duration-500 ease-in-out">
    <div class="p-6 flex flex-col items-center justify-center border-b border-gray-700">
      <img src="{{ url_for('static', filename='images/login-logo.png') }}" 
           alt="ParkFast Logo" 
           class="h-16 md:h-20 object-contain rounded-xl shadow-lg" />
      <span class="mt-3 text-white text-xl custom-font tracking-wide">ParkFast</span>
    </div>
    <nav class="flex-1 p-6 space-y-4">
      <a href="/dashboard" class="block py-2 px-4 rounded-lg hover:bg-[#1f2937] transition-all duration-300"><i class="fas fa-tachometer-alt mr-2"></i> Dashboard</a>
      <a href="/about" class="block py-2 px-4 rounded-lg hover:bg-[#1f2937] transition-all duration-300"><i class="fas fa-info-circle mr-2"></i> About</a>
      <a href="/contact" class="block py-2 px-4 rounded-lg hover:bg-[#1f2937] transition-all duration-300"><i class="fas fa-envelope mr-2"></i> Contact</a>
      <a href="/help" class="block py-2 px-4 rounded-lg hover:bg-[#1f2937] transition-all duration-300"><i class="fas fa-question-circle mr-2"></i> Help</a>
<a href="/live_parking" class="block py-2 px-4 rounded-lg hover:bg-[#1f2937] transition-all duration-300">
    <i class="fas fa-question-circle mr-2"></i> Live Update
</a>      <a href="/parking_logs" class="block py-2 px-4 rounded-lg hover:bg-[#1f2937] transition-all duration-300">
  <i class="fas fa-history mr-2"></i> Parking History
</a>
    </nav>
    <div class="p-6 border-t border-gray-700">
      <a href="/logout" class="w-full block text-center bg-gradient-to-r from-red-500 to-pink-500 hover:from-pink-500 hover:to-red-500 py-2 rounded-lg font-bold transition-all duration-300">
        <i class="fas fa-sign-out-alt"></i> Logout
      </a>
    </div>
  </aside>

  <!-- Main content -->
  <div class="flex-1 flex flex-col overflow-y-auto">

    <!-- Top Navbar -->
    <header class="bg-white shadow-md p-6 flex justify-between items-center sticky top-0 z-50">
      <h1 class="text-2xl font-bold text-gray-700">Hey, {{ session['user'] }} 👋</h1>
      <button onclick="refreshSlots()" class="bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-indigo-500 hover:to-blue-500 text-white px-5 py-2 rounded-full font-semibold transition-all duration-300 shadow-md">
        🔄 Refresh Slots
      </button>
    </header>

    <!-- Dashboard Content -->
    <main class="p-8 space-y-8">

      <!-- Info Cards -->
      <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div class="bg-gradient-to-r from-blue-400 to-blue-600 p-6 rounded-xl shadow-lg text-white flex flex-col items-center transform hover:scale-105 transition duration-300">
          <i class="fas fa-parking text-4xl mb-4"></i>
          <div class="text-lg font-bold">Real-Time Availability</div>
        </div>
        <div class="bg-gradient-to-r from-green-400 to-green-600 p-6 rounded-xl shadow-lg text-white flex flex-col items-center transform hover:scale-105 transition duration-300">
          <i class="fas fa-credit-card text-4xl mb-4"></i>
          <div class="text-lg font-bold">FASTag Payments</div>
        </div>
        <div class="bg-gradient-to-r from-purple-400 to-purple-600 p-6 rounded-xl shadow-lg text-white flex flex-col items-center transform hover:scale-105 transition duration-300">
          <i class="fas fa-chart-line text-4xl mb-4"></i>
          <div class="text-lg font-bold">Predictive Analytics</div>
        </div>
        <div class="bg-gradient-to-r from-yellow-400 to-yellow-600 p-6 rounded-xl shadow-lg text-white flex flex-col items-center transform hover:scale-105 transition duration-300">
          <i class="fas fa-traffic-light text-4xl mb-4"></i>
          <div class="text-lg font-bold">Efficient Traffic Flow</div>
        </div>
      </section>

      <!-- Mall Parking Selection -->
      <section class="bg-white p-8 rounded-xl shadow-md">
        <h2 class="text-3xl font-extrabold mb-8 text-center text-gray-800">🛴 Select a Mall</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">

          <div onclick="checkAvailability('Phoenix Mall')" class="cursor-pointer bg-gray-100 hover:bg-blue-100 p-6 rounded-lg shadow flex flex-col items-center transform hover:scale-105 transition-all duration-300">
            <h4 class="text-xl font-bold">Phoenix Mall</h4>
            <p class="text-green-600 text-2xl font-bold mt-2">8 Slots</p>
          </div>

          <div onclick="checkAvailability('Express Avenue')" class="cursor-pointer bg-gray-100 hover:bg-blue-100 p-6 rounded-lg shadow flex flex-col items-center transform hover:scale-105 transition-all duration-300">
            <h4 class="text-xl font-bold">Express Avenue</h4>
            <p class="text-green-600 text-2xl font-bold mt-2">8 Slots</p>
          </div>

          <div onclick="checkAvailability('VR Chennai')" class="cursor-pointer bg-gray-100 hover:bg-blue-100 p-6 rounded-lg shadow flex flex-col items-center transform hover:scale-105 transition-all duration-300">
            <h4 class="text-xl font-bold">VR Chennai</h4>
            <p class="text-red-500 text-2xl font-bold mt-2">Full</p>
          </div>

          <div onclick="checkAvailability('Ampa Skywalk')" class="cursor-pointer bg-gray-100 hover:bg-blue-100 p-6 rounded-lg shadow flex flex-col items-center transform hover:scale-105 transition-all duration-300">
            <h4 class="text-xl font-bold">Ampa Skywalk</h4>
            <p class="text-yellow-500 text-2xl font-bold mt-2">5 Slots</p>
          </div>

        </div>

        <div class="mt-10" id="selected-mall">
          <!-- Dynamic mall slots will load here -->
        </div>
      </section>

      <!-- Parking Logs -->
<section class="bg-white p-8 rounded-xl shadow-md mt-10">
  <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">📄 Recent Parking Logs</h2>

  <div id="parking-logs">
    <!-- Parking log entries will be loaded here by JavaScript -->
  </div>
</section>


    </main>

    <!-- Footer -->
    <footer class="bg-gray-100 text-center p-6 text-sm text-gray-600 mt-auto shadow-inner">
      &copy; 2025 <span class="font-semibold text-gray-800">ParkFast</span>. Empowering your parking experience 🚀
    </footer>

  </div>

  <script>
  let currentMall = "";

  function checkAvailability(mallName) {
    currentMall = mallName;
    fetchSlots(mallName);
  }

  function fetchSlots(mallName) {
    const output = document.getElementById("selected-mall");
    output.innerHTML = `<p class='text-gray-600 text-center'>Loading slots at <strong>${mallName}</strong>...</p>`;

    fetch(`/slots?mall=${encodeURIComponent(mallName)}`)
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          output.innerHTML = "<p class='text-red-500 text-center'>Error fetching slots!</p>";
          return;
        }

        let html = `<h3 class='text-2xl font-bold text-center text-gray-800 mb-8'>🚗 ${mallName} - Live Slots</h3><div class='grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6'>`;

        data.forEach(slot => {
          const isOccupied = slot.status === "occupied";
          const bgColor = isOccupied ? "bg-red-500" : "bg-green-500";
          const icon = isOccupied ? "fas fa-car-crash" : "fas fa-parking";
          const status = isOccupied ? "Occupied" : "Available";

          html += `
            <div class='flex flex-col items-center justify-center p-4 rounded-xl shadow ${bgColor} text-white transform hover:scale-105 transition-all'>
              <i class='${icon} text-3xl mb-2'></i>
              <div class='font-bold'>Slot ${slot.slot}</div>
              <small>${status}</small>
            </div>
          `;
        });

        html += `</div>`;
        output.innerHTML = html;
      })
      .catch(err => {
        output.innerHTML = "<p class='text-red-500 text-center'>Server error!</p>";
      });
  }

  function refreshSlots() {
    if (currentMall) {
      fetchSlots(currentMall);
    }
  }
window.addEventListener('load', () => {
  const popup = document.getElementById('welcomePopup');
  popup.classList.remove('hidden');
});

function closePopup() {
  const popup = document.getElementById('welcomePopup');
  popup.classList.add('hidden');
}

// Close when ESC key is pressed
window.addEventListener('keydown', (event) => {
  if (event.key === "Escape") {  // If ESC key is pressed
    closePopup();
  }
});

function loadParkingLogs() {
  fetch("/api/parking_logs")
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById("parking-logs");

      if (data.length === 0) {
        container.innerHTML = `<p class="text-center text-gray-500">No parking logs available.</p>`;
        return;
      }

      let html = `
        <div class="overflow-x-auto">
          <table class="min-w-full table-auto text-center border border-gray-200 rounded">
            <thead class="bg-gray-100 text-gray-700 uppercase text-sm">
              <tr>
                <th class="px-6 py-3">Mall</th>
                <th class="px-6 py-3">In-Time</th>
                <th class="px-6 py-3">Out-Time</th>
                <th class="px-6 py-3">Fare (₹)</th>
              </tr>
            </thead>
            <tbody class="text-gray-700 text-sm font-light">
      `;

      data.forEach(log => {
        html += `
          <tr class="border-b border-gray-200 hover:bg-gray-100">
            <td class="px-6 py-4">${log.mall_name}</td>
            <td class="px-6 py-4">${log.in_time}</td>
            <td class="px-6 py-4">${log.out_time}</td>
            <td class="px-6 py-4">${log.fare}</td>
          </tr>
        `;
      });

      html += `</tbody></table></div>`;
      container.innerHTML = html;
    })
    .catch(error => {
      console.error("Error fetching parking logs:", error);
      document.getElementById("parking-logs").innerHTML = `<p class="text-red-500 text-center">Failed to load logs.</p>`;
    });
}

// Load logs when page loads
window.addEventListener("load", loadParkingLogs);




  </script>

</body>
</html>
"""


about_page = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Us</title>
    
    <!-- Correct way to load Tailwind CSS -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">

    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
    </style>
</head>
<body class="bg-gray-50 min-h-screen flex flex-col">

    <!-- Navigation -->
    <nav class="bg-blue-600 text-white p-4">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-xl font-bold">ParkFast</a>
            <div class="space-x-4">
                <a href="/" class="hover:text-gray-300">Home</a>
                <a href="/about" class="hover:text-gray-300">About</a>
                <a href="/contact" class="hover:text-gray-300">Contact</a>
            </div>
        </div>
    </nav>

    <!-- About Section -->
    <section class="flex-grow py-16 bg-white">
        <div class="container mx-auto px-4 text-center">
            <h2 class="text-4xl font-bold text-blue-600 mb-6">About Us</h2>
            <p class="text-lg text-gray-700 mb-4">
                Welcome to ParkFast, where we strive to make parking smarter and more convenient for everyone.
            </p>
            <p class="text-lg text-gray-700 mb-8">
                We are dedicated to helping you find and reserve parking spots across various locations in Chennai, including Phoenix Mall, Express Avenue, VR Mall, and more. Our goal is to reduce the stress of parking by offering a seamless experience for users to park, pay, and go.
            </p>
            <div class="flex justify-center">
                <div class="w-full sm:w-1/2 md:w-1/3">
                    <img src="https://www.shutterstock.com/image-vector/vector-icon-parking-cars-sign-600nw-2490009635.jpg" alt="ParkFast Logo" class="rounded-lg shadow-lg w-full">
                </div>
            </div>
        </div>
    </section>

    <!-- Our Mission Section -->
    <section class="py-16 bg-gray-100">
        <div class="container mx-auto px-4 text-center">
            <h3 class="text-3xl font-semibold text-blue-600 mb-4">Our Mission</h3>
            <p class="text-lg text-gray-700 mb-8">
                Our mission is to make parking easier, faster, and more accessible for everyone. With our innovative platform, we aim to reduce the time spent searching for parking and offer a more efficient, stress-free parking experience.
            </p>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-blue-600 text-white p-6">
        <div class="container mx-auto text-center">
            <p>&copy; 2025 ParkFast. All rights reserved.</p>
            <p>Need help? <a href="mailto:support@parkfast.in" class="underline hover:text-gray-300">Contact us</a>.</p>
        </div>
    </footer>

</body>
</html>

"""

base_tailwind = """<script src="https://cdn.tailwindcss.com"></script>"""

forgot_template = base_tailwind + """
<body class="bg-gray-202427 flex items-center justify-center min-h-screen">
<div class="max-w-md w-full bg-white rounded-xl shadow-lg p-6">
    <h2 class="text-2xl font-semibold mb-6 text-center text-gray-800">Forgot Password</h2>
    <form method="POST" class="space-y-6">
        <input name="email" type="email" placeholder="Enter your email" class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
        <button type="submit" class="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500">Send OTP</button>
    </form>
</div>
</body>
"""

otp_template = base_tailwind + """
<body class="bg-gray-202427 flex items-center justify-center min-h-screen">
<div class="max-w-md w-full bg-white rounded-xl shadow-lg p-6">
    <h2 class="text-2xl font-semibold mb-6 text-center text-gray-800">Verify OTP</h2>
    <form method="POST" action="/verify_otp" class="space-y-6">
        <input type="hidden" name="email" value="{{ email }}">
        <input name="otp" type="text" placeholder="Enter OTP" class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
        <button type="submit" class="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 focus:ring-2 focus:ring-green-500">Verify OTP</button>
    </form>
</div>
</body>
"""

new_password_template = base_tailwind + """
<body class="bg-gray-202427 flex items-center justify-center min-h-screen">
<div class="max-w-md w-full bg-white rounded-xl shadow-lg p-6">
    <h2 class="text-2xl font-semibold mb-6 text-center text-gray-800">Reset Password</h2>
    <form method="POST" action="/reset_password" class="space-y-6">
        <input type="hidden" name="email" value="{{ email }}">
        <input name="password" type="password" placeholder="Enter new password" class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
        <button type="submit" class="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 focus:ring-2 focus:ring-purple-500">Reset Password</button>
    </form>
</div>
</body>
"""





# ------------------- Routes -------------------


@app.route('/')
def landing_page():
    landing_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ParkFast - Find Your Parking Instantly</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    /* Body and background setup */
    body {
      font-family: 'Poppins', sans-serif;
      color: #0f172a;
      overflow-x: hidden;
      height: 100vh;
      background: url('{{ url_for("static", filename="images/background.png") }}') no-repeat center center fixed;
      background-size: cover;
    }

    /* Overlay with transparency */
    .overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.4); /* Black overlay with 40% opacity */
      z-index: 1;
    }

    /* Content in the page */
    .content {
      position: relative;
      z-index: 2; /* This makes sure content appears on top of the overlay */
      text-align: center;
      padding: 50px 20px;
      color: white;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .navbar {
      position: fixed;
      top: 20px;
      right: 30px;
      z-index: 3;
    }
    .navbar a {
      text-decoration: none;
      background: white;
      color: #0ea5e9;
      padding: 10px 20px;
      border-radius: 20px;
      font-weight: 600;
      transition: 0.3s;
      font-size: 16px;
    }
    .navbar a:hover {
      background: #0f172a;
      color: white;
    }

    header h1 {
      font-size: 50px;
      margin-bottom: 20px;
      animation: fadeInDown 1s ease-out;
    }
    header p {
      font-size: 20px;
      margin-bottom: 30px;
      animation: fadeInUp 1.2s ease-out;
    }
    header a.explore-btn {
      background: white;
      color: #0ea5e9;
      padding: 15px 30px;
      font-size: 18px;
      border-radius: 30px;
      text-decoration: none;
      font-weight: 600;
      transition: 0.3s;
      animation: fadeInUp 1.5s ease-out;
    }
    header a.explore-btn:hover {
      background: #0f172a;
      color: white;
    }

    section {
      padding: 60px 20px;
      max-width: 1200px;
      margin: auto;
    }
    .features {
      display: flex;
      flex-wrap: wrap;
      gap: 40px;
      justify-content: center;
      margin-bottom: 50px;
    }
    .feature {
      background: white;
      padding: 30px;
      border-radius: 20px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
      flex: 1 1 300px;
      text-align: center;
      transition: 0.3s;
    }
    .feature:hover {
      transform: translateY(-10px);
    }
    .feature h3 {
      margin-bottom: 10px;
      color: #0ea5e9;
    }
    .feature p {
      font-size: 16px;
      color: #64748b;
    }

    footer {
      text-align: center;
      padding: 30px;
      font-size: 14px;
      color: #94a3b8;
      margin-top: 30px;
    }

    /* Animations */
    @keyframes fadeInDown {
      from { opacity: 0; transform: translateY(-30px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(30px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @media(max-width: 768px) {
      header h1 { font-size: 32px; }
      header p { font-size: 16px; }
      header a.explore-btn { font-size: 16px; }
    }
  </style>
</head>

<body>

<!-- Overlay for transparency -->
<div class="overlay"></div>

<!-- Content -->
<div class="content">
  <!-- Navbar -->
  <div class="navbar">
    <a href="/login">Login</a>
  </div>

  <!-- Hero Section -->
  <header>
    <h1>ParkFast</h1>
    <p>Find, Book, and Park — Smarter and Faster</p>
    <a href="/signup" class="explore-btn">Explore</a>
  </header>

 
 <!-- <section>
    <h2 style="text-align: center; margin-bottom: 40px;">Why Choose ParkFast?</h2>
    <div class="features">
      <div class="feature">
        <h3>Real-time Availability</h3>
        <p>See which slots are free in real-time and book instantly.</p>
      </div>
      <div class="feature">
        <h3>Secure Payments</h3>
        <p>Fast and secure online payments without any hassles.</p>
      </div>
      <div class="feature">
        <h3>Navigate Easily</h3>
        <p>Integrated Google Maps to guide you to your parking spot.</p>
      </div>
    </div>
  </section> --!>

  <!-- Footer -->
  <footer>
    © 2025 ParkFast. All rights reserved.
  </footer>
</div>

</body>
</html>

 """
    return render_template_string(landing_html)

@app.route("/signup")
def home():
    return render_template_string(signup_page)

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = generate_password_hash(password)

    # ✅ Configure Mail settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'rudran.development@gmail.com'           # Replace with your Gmail
    app.config['MAIL_PASSWORD'] = 'dyfl dcrv fcrw nerb'             # Use Gmail App Password
    app.config['MAIL_DEFAULT_SENDER'] = 'rudran.development@gmail.com'     # Same as username

    mail = Mail(app)

    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost", user="Rudran", password="Rudran@2005", database="sps_project"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            flash("Email already exists! Try logging in.")
            return redirect(url_for("home"))

        # Insert into DB
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        conn.commit()

        # ✅ Send Welcome Email
        msg = Message("Welcome to ParkFast!", recipients=[email])
        msg.html =  f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome to ParkFast</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f5;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 30px auto;
            background: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        .header {{
            background-color: #0f172a;
            text-align: center;
            padding: 30px;
        }}
        .header img {{
            width: 120px;
            margin-bottom: 10px;
        }}
        .header h1 {{
            color: #ffffff;
            font-size: 26px;
            margin: 0;
        }}
        .content {{
            padding: 30px;
            text-align: center;
        }}
        .content h2 {{
            color: #0f172a;
            font-size: 22px;
            margin-bottom: 15px;
        }}
        .content p {{
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
        }}
        .button {{
            display: inline-block;
            background-color: #0f172a;
            color: #ffffff;
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 6px;
            font-weight: 600;
        }}
        .footer {{
            background-color: #f1f5f9;
            padding: 20px;
            text-align: center;
            font-size: 14px;
            color: #6b7280;
        }}
        .footer a {{
            color: #0f172a;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://www.shutterstock.com/image-vector/vector-icon-parking-cars-sign-600nw-2490009635.jpg" alt="ParkFast Logo">
            <h1>Welcome, {name}!</h1>
        </div>
        <div class="content">
            <h2>🚗 Park Smarter. Drive Happier.</h2>
            <p>We’re thrilled to welcome you to <strong>ParkFast</strong> — Chennai’s most intelligent parking assistant. No more circling for spots. No more stress.</p>
            <p>Find and reserve parking across Phoenix Mall, Express Avenue, VR Mall and more — all in one place.</p>
            <a class="button" href="http://localhost:5000/login">Login Now</a>
        </div>
        <div class="footer">
            Need help? Email us at 
            <a href="mailto:support@parkfast.in">support@parkfast.in</a><br><br>
            &copy; 2025 ParkFast · All rights reserved
        </div>
    </div>
</body>
</html>
"""

        mail.send(msg)

        flash(" Sign-up successful! You can now login")
        return redirect(url_for("login"))

    except Error as e:
        flash(f"Database error: {str(e)}")
        return redirect(url_for("home"))

    finally:
        if conn and conn.is_connected():
            cur.close()
            conn.close()

@app.route("/login")
def login():
    return render_template_string(login_page)


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT name, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user[1], password):
            session["user"] = user[0]
            flash("Login successful!")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.")
            return redirect(url_for("login"))
    except Error as e:
        flash(f"Login error: {str(e)}")
        return redirect(url_for("login"))
    finally:
        if conn and conn.is_connected():
            cur.close()
            conn.close()

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template_string(dashboard_page)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.")
    return redirect(url_for("login"))

@app.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form['email']
        otp = str(random.randint(100000, 999999))
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET otp = %s WHERE email = %s", (otp, email))
        conn.commit()
        cursor.close()
        conn.close()

        sent = send_otp_email(email, otp)
        if not sent:
            return "Email sending failed. Check your email and credentials."
        
        return render_template_string(otp_template, email=email)
    return render_template_string(forgot_template)

@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    email = request.form['email']
    user_otp = request.form['otp']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT otp FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and result[0] == user_otp:
        return render_template_string(new_password_template, email=email)
    else:
        return "Invalid OTP. Please try again."

@app.route("/reset_password", methods=["POST"])
def reset_password():
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = %s, otp = NULL WHERE email = %s", (hashed_password, email))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("login"))

@app.route("/slots")
def get_slots():
    mall_name = request.args.get("mall")

    if not mall_name:
        return jsonify({"error": "Mall name is required"}), 400

    try:
        print(f"Mall requested: {mall_name}")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT slot_number, status FROM parking_slots WHERE mall_name = %s", (mall_name,))
        data = cursor.fetchall()
        cursor.close()

        print(f"DB Result: {data}")

        if not data:
            return jsonify({"error": "No slots found for this mall"}), 404

        slots = [{"slot": row[0], "status": row[1]} for row in data]
        return jsonify(slots)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/about")
def about():
    return render_template_string(about_page)



@app.route("/api/parking_logs")
def api_parking_logs():
    if "user" not in session:
        return jsonify([])

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT mall_name, in_time, out_time, fare
            FROM parking_logs
            WHERE user_name = %s
            ORDER BY in_time DESC
        """, (session["user"],))
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(logs)
    except Exception as e:
        print("Error fetching logs:", e)
        return jsonify([])



# ------------------- Run App -------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


