from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime
import pytz

# Initialize attendance tracking
attendance = {}
course_weeks = 6  # Number of weeks in the course

# Helper to get current week number
def get_week_number():
    today = datetime.datetime.now(pytz.timezone('Asia/Riyadh'))  # Adjust timezone to your local time
    course_start_date = datetime.datetime(2025, 1, 14, tzinfo=pytz.timezone('Asia/Riyadh'))  # Course start date
    week_number = (today - course_start_date).days // 7 + 1
    return week_number if 1 <= week_number <= course_weeks else None

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    if user_id not in attendance:
        attendance[user_id] = {"name": username, "attendance": []}
        await update.message.reply_text("تم تسجيلك بنجاح.")
    else:
        await update.message.reply_text("أنت مسجل بالفعل!")

# Mark attendance
async def mark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    week_number = get_week_number()
    if week_number is None:
        await update.message.reply_text("الوقت الحالي ليس ضمن أيام الدورة.")
        return

    if user_id in attendance:
        if week_number in attendance[user_id]["attendance"]:
            await update.message.reply_text("لقد قمت بتسجيل الحضور لهذا الأسبوع بالفعل.")
        else:
            attendance[user_id]["attendance"].append(week_number)
            await update.message.reply_text("تم تسجيل حضورك لهذا الأسبوع.")
    else:
        await update.message.reply_text("الرجاء استخدام /start أولاً لتسجيل اسمك.")

# Generate attendance report
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    report_text = "تقرير الحضور:\n\n"
    for user_id, info in attendance.items():
        weeks_attended = sum(info["attendance"])
        report_text += f"{info['name']}: حضر {weeks_attended} من {course_weeks} أسبوعًا.\n"
    await update.message.reply_text(report_text)

# Main function
def main():
    app = Application.builder().token("7933750959:AAEd5PVhRvyL8SUZD0ZvB5UVyBnK0VGAINM").build()  # Replace with your BotFather token

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mark", mark))
    app.add_handler(CommandHandler("report", report))

    app.run_polling()

if __name__ == "__main__":
    main()
