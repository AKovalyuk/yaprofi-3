from dataclasses import dataclass

from russiannames.parser import NamesParser


@dataclass
class Record:
    surname: str
    name: str
    patronymic: str


def get_parts(user_input: str) -> tuple[str | None, str | None, str | None] | str:
    """
    Возвращает ФИО человека,
    либо (в случае введенных не до конца данных) - сам ввод пользователя
    во избежание ложной детекции как фамилия
    """
    if len(user_input.split()) < 2:
        return user_input
    parse_result = NamesParser().parse(user_input)
    return (
        parse_result.get('sn'),
        parse_result.get('fn'),
        parse_result.get('mn'),
    )


db = {
    0: Record("Иванов", "Иван", "Иванович"),
    1: Record("Иванов", "Петр", "Васильевич"),
    2: Record("Мальцев", "Денис", "Константинович"),
    3: Record("Примеров", "Андрей", "Васильевич"),
    4: Record("Андреев", "Иван", "Васильевич"),
    5: Record("Зверев", "Петр", "Васильевич"),
}


def find_in_db(user_input: str, db: dict[int, Record]) -> list[tuple[int, Record]]:
    result = []
    parts = get_parts(user_input)
    if isinstance(parts, str):
        parts = parts.lower()
        for id, record in db.items():
            if record.surname.lower().startswith(parts) \
                or record.name.lower().startswith(parts) \
                or record.patronymic.lower().startswith(parts):
                result.append((id, record))
    else:
        parts = tuple((part.lower() if part else None) for part in parts)
        for id, record in db.items():
            if (not parts[0] or record.surname.lower().startswith(parts[0])) \
                and (not parts[1] or record.name.lower().startswith(parts[1])) \
                    and (not parts[2] or record.patronymic.lower().startswith(parts[2])):
                result.append((id, record))
    return result


if __name__ == "__main__":
    user_input = input("Ввод пользователя: ")
    print("Найдены записи:")
    for id, record in find_in_db(user_input, db):
        print(f"{id}, {record}")
