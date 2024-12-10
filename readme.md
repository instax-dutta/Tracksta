# TrackSta: The Ultimate Discord Activity Tracker Bot  

TrackSta is a robust Discord bot designed to monitor and track server members' activity, including online/offline status and gaming sessions. It helps moderators and members maintain a healthy balance between fun and productivity by providing detailed activity reports and timely reminders.

---

## Features  

- **Activity Tracking**: Logs every user's online and offline times, along with session durations.  
- **Gaming Session Monitoring**: Tracks the games users play and their duration for each session.  
- **Break Reminders**: Notifies users in the general chat to take breaks if they’ve been playing for more than 2 hours. Messages auto-delete after 5 minutes.  
- **Weekly Reports**:  
  - Sends a personalized weekly activity report to each user via DM.  
  - Delivers a comprehensive master report to the moderators’ channel.  
- **Robust Data Handling**: Ensures accurate logging of all user activities without bypasses.  
- **Single-Server Design**: Optimized for managing detailed data in a single-server environment.  

---

## Prerequisites  

- Python 3.8–3.11  
- A MongoDB instance for storing user activity logs  
- Discord bot token  
- Permissions for the bot to manage messages, send messages, and access member activities  

---

## Installation  

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/instax-dutta/TrackSta.git
   cd TrackSta
   ```  

2. **Install Dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```  

3. **Set Up MongoDB**:  
   - Create a database for TrackSta.  
   - Update the `MONGO_URI` in the code with your MongoDB connection string.  

4. **Configure Bot Token**:  
   - Replace the `BOT_TOKEN` in the code with your Discord bot token.  

5. **Run the Bot**:  
   ```bash
   python main.py
   ```  

---

## Configuration  

- **General Chat ID**: Update the `general_channel_id` in the code with your server's general chat channel ID.  
- **Moderator Channel ID**: Set the `moderator_channel_id` for sending the master activity report.  

---

## Usage  

- Add TrackSta to your server and ensure it has the necessary permissions.  
- The bot will automatically start logging member activities and send reminders/reports as scheduled.  

---

## Roadmap  

- Add support for tracking more activities like voice channel participation.  
- Implement user-configurable break reminders.  
- Add multi-server support in future versions.  

---

## Contributing  

We welcome contributions! Please fork the repository and submit a pull request with your changes.  

---

## License  

This project is licensed under the MIT License. See the `LICENSE` file for more details.  

---

## Contact  

For questions or issues, feel free to open an issue or contact the repository owner at **contact@sdad.pro**.  

---

Happy Tracking with **TrackSta**! 🎮✨