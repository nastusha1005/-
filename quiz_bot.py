question = random.choice(QUIZ_DATA)
    
    # Рассылка вопроса
    for team_name, team_data in game.teams.items():
        expert_id = random.choice(team_data["members"])
        
        for user_id in team_data["members"]:
            is_expert = (user_id == expert_id)
            options = prepare_options(question, is_expert)
            
            context.bot.send_message(
                chat_id=user_id,
                text=f"🎯 <b>Раунд {game.current_round}/{ROUNDS}</b>\n"
                     f"{question['question']}\n\n"
                     f"⏱ У вас 20 секунд!",
                reply_markup=create_keyboard(options, team_name),
                parse_mode=ParseMode.HTML
            )
    
    # Таймер на ответ
    context.job_queue.run_once(
        end_round, 
        20, 
        context=game.current_round
    )

def end_round(context: CallbackContext):
    game.current_round += 1
    start_round(context)

def end_game(context: CallbackContext):
    # Финал и статистика
    game.state = "ended"
    # ... (логика завершения)

def main():
    TOKEN = "7573442590:AAFjhICMNH7D_WehdtnZugnD-C0kg0Ji_FI"
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("join", join))
    dp.add_handler(CommandHandler("spectate", spectate))
    dp.add_handler(CallbackQueryHandler(handle_answer))
    
    updater.start_polling()
    updater.idle()

if name == "main":
    main()
