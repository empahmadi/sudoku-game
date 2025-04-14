def get_border_style(row, col):
    border_style = "border: 1px solid #999;"

    if row % 3 == 0:
        border_style += "border-top: 3px solid #000;"
    if col % 3 == 0:
        border_style += "border-left: 3px solid #000;"
    if row == 8:
        border_style += "border-bottom: 3px solid #000;"
    if col == 8:
        border_style += "border-right: 3px solid #000;"

    return border_style


def update_stats(level, status):
    if level == 0:
        difficulty = "easy"
    elif level == 1:
        difficulty = "medium"
    elif level == 2:
        difficulty = "hard"
    else:
        return False

    with open("assets/profile/stat.txt", 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith(difficulty + ':'):
            _, values = line.strip().split(':')
            total, wins = map(int, values.split('-'))
            total += 1

            if status:
                wins += 1

            lines[i] = f"{difficulty}:{total}-{wins}\n"
            break

    with open("assets/profile/stat.txt", 'w') as f:
        f.writelines(lines)


def get_stats():
    with open("assets/profile/stat.txt", 'r') as f:
        lines = f.readlines()

    stats = {}

    for i, line in enumerate(lines):
        difficulty, values = line.strip().split(':')
        total, wins = map(int, values.split('-'))
        level = {
            "total": total,
            "wins": wins
        }
        stats[difficulty] = level

    return stats
