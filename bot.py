import json
import os
import shutil

from pdf2image import convert_from_path
from requests import get
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup

TOKEN = "1116820230:AAHm6C00UvlPDOk-NAnT1kPgftMPuzI-CG4"


def pdf2jpg(source, destination, standart):
    images = convert_from_path(source)

    for i in range(len(images)):
        # Save pages as images in the pdf
        add = ""
        if standart:
            add = "_" + str(i + 1)
        images[i].save(destination + add + ".jpg", 'JPEG')
        if not standart:
            break


def upload(update, context):
    file_id = update.message.document.file_id
    telegram_link = 'https://api.telegram.org/bot' + TOKEN + '/getFile?file_id=' + file_id
    response = get(telegram_link).json()
    telegram_document_link = 'https://api.telegram.org/file/bot' + TOKEN + '/' + response["result"]["file_path"]
    photo = get(telegram_document_link)
    if photo.status_code == 200:
        if str(update.message.caption).strip().lower() == "стандартное":
            with open(f"files/standart_timetable.pdf", 'wb') as f:
                for chunk in photo:
                    f.write(chunk)
            pdf2jpg("files/standart_timetable.pdf", "files/standart_timetable", 1)
            os.remove("files/standart_timetable.pdf")
        else:
            with open(f"files/timetable_{update.message.caption}.pdf", 'wb') as f:
                for chunk in photo:
                    f.write(chunk)
            pdf2jpg(f"files/timetable_{update.message.caption}.pdf", f"files/timetable_{update.message.caption}", 0)
            os.remove(f"files/timetable_{update.message.caption}.pdf")
        update.message.reply_text("Расписание добавлено.")


def start(update, context):
    update.message.reply_text("Здравствуйте. \nЭто бот терминала.\n"
                              "Для начала работы необходимо добавить стандартное расписание на неделю.\n"
                              "Для этого отправьте сообщение с текстом \"стандартное\", прикрепив pdf-файл.\n"
                              "Вы можете загрузить расписание на конкретный день, оправив сообщение в формате дд.мм.гггг и прикрепив pdf-файл\n"
                              )
    return 1


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        fallbacks=[],
        states={
            1: [MessageHandler(Filters.all, upload)]
        }
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
