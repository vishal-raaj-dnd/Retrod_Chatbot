def get_whatsapp_main_menu(profile_name: str) -> str:
    """
    Returns WhatsApp Main Menu with interactive command triggers and numbered action buttons.
    """
    return (
        f"👋 Hi *{profile_name}*! Welcome to *Retrod PMS Assistant*.\n\n"
        "Reply with a number or tap an action:\n\n"
        "1️⃣ 📊 *Today's Revenue*\n"
        "2️⃣ 🏨 *Room Occupancy*\n"
        "3️⃣ 🔑 *Today's Check-ins*\n"
        "4️⃣ 🟢 *PMS Backend Health*\n"
        "5️⃣ 🌐 *New Reservation Link*\n\n"
        "💡 _Or ask me any question about PMS workflows or page links!_"
    )
