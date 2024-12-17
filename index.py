import streamlit as st
import pickle
import os
import json

# Пусть имя файла для схем будет постоянным
SCHEMA_FILE = "schemas.pkl"

# Функция для загрузки схем
def load_schemas():
    if os.path.exists(SCHEMA_FILE):
        with open(SCHEMA_FILE, "rb") as f:
            return pickle.load(f)
    return {}

# Функция для сохранения схем
def save_schemas(schemas):
    with open(SCHEMA_FILE, "wb") as f:
        pickle.dump(schemas, f)

# Реализуем delete_schema
def delete_schema(name):
    schemas = load_schemas()
    if name not in schemas:
        st.error(f"Схема с именем '{name}' не найдена.")
        return
    del schemas[name]
    save_schemas(schemas)
    st.success(f"Схема '{name}' успешно удалена.")

# Реализуем merge_schemas
def merge_schemas(files):
    merged_schemas = load_schemas()
    for file in files:
        try:
            with open(file, "rb") as f:
                new_schemas = pickle.load(f)

            for name, schema in new_schemas.items():
                if name in merged_schemas:
                    new_name = st.text_input(
                        f"Имя '{name}' конфликтует. Введите новое имя для объединения:",
                        f"{name}_merged",
                        key=name,
                    )
                    merged_schemas[new_name] = schema
                else:
                    merged_schemas[name] = schema
        except Exception as e:
            st.error(f"Ошибка при обработке файла {file}: {e}")

    save_schemas(merged_schemas)
    st.success("Все схемы успешно объединены и сохранены.")

# Новый функционал: создание схем
def create_new_schema(name, schema_content):
    schemas = load_schemas()
    if name in schemas:
        st.error(f"Схема с именем '{name}' уже существует. Выберите другое имя.")
        return
    try:
        parsed_schema_content = json.loads(schema_content)
        schemas[name] = parsed_schema_content
        save_schemas(schemas)
        st.success(f"Схема '{name}' успешно создана и сохранена.")
    except json.JSONDecodeError:
        st.error("Содержимое схемы не является корректным JSON. Попробуйте снова.")

# Новый функционал: отображение содержимого схем
def display_schemas():
    schemas = load_schemas()
    if schemas:
        for name, content in schemas.items():
            with st.expander(f"Схема: {name}", expanded=False):
                st.json(content)
    else:
        st.write("Нет сохранённых схем для отображения.")

# Основной интерфейс Streamlit
def main(schema_content=None):
    st.set_page_config(page_title="Управление схемами", page_icon="📊", layout="wide")

    # Кастомные стили
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #90ee90; /* Зеленый фон */
            color: black; /* Цвет текста */
            font-family: 'Arial', sans-serif;
        }
        h1, h2, h3 {
            color: black; /* Цвет заголовков */
            text-align: center;
        }
        input, textarea {
            color: black; /* Цвет текста в полях ввода */
        }
        .stButton > button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        .sidebar .sidebar-content {
            background-color: #007bff;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Управление Node-based схемами")

    st.header("Загрузка и просмотр схем")
    schemas = load_schemas()
    if schemas:
        st.write("Сохранённые схемы:")
        for name in schemas.keys():
            st.write(f"• {name}")

        st.header("📜 Отобразить содержимое схем")
        display_schemas()
    else:
        st.write("Нет сохранённых схем.")

    st.header("Удаление схемы")
    schema_to_delete = st.text_input("Введите имя схемы для удаления:")
    if st.button("Удалить"):
        delete_schema(schema_to_delete)

    st.header("Объединение схем")
    uploaded_files = st.file_uploader(
        "Загрузите файлы с сохранёнными схемами:", accept_multiple_files=True
    )
    if st.button("Объединить"):
        if uploaded_files:
            file_paths = []
            for uploaded_file in uploaded_files:
                temp_file_path = f"temp_{uploaded_file.name}"
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_paths.append(temp_file_path)

            merge_schemas(file_paths)

            for path in file_paths:
                os.remove(path)
        else:
            st.error("Пожалуйста, загрузите хотя бы один файл.")

    st.header("Сохранить схему")
    new_name = st.text_input("Введите имя для новой схемы:")
    new_schema = st.text_area("Введите содержимое схемы (json или структура):")
    if st.button("Сохранить"):
        if new_name and new_schema:
            create_new_schema(new_name, new_schema)
        else:
            st.error("Заполните все поля перед сохранением.")

    st.header("Создание новой схемы")
    schema_name = st.text_input("Введите имя для создаваемой схемы:")
    st.header("Пример данных схемы")
    st.code(
        '''
        {
        'nodes': [
          {
            'type': 'Feed', 
            'id': 'node_17341976050490', 
            'name': 'Feed-1', 
            'options': [], 
            'state': {}, 
            'interfaces': [[
              'Output 1', 
              {
                'id': 'ni_17341976050491', 
                'value': None
              }
            ]], 
            'position': {
              'x': 41.089179548156956, 
              'y': 233.22473246135553
            }, 
              'width': 200, 
              'twoColumn': False, 
              'customClasses': ''
            }, 
            {
              'type': 'Result', 
              'id': 'node_17341976077762', 
              'name': 'Result-1', 
              'options': [], 
              'state': {}, 
              'interfaces': [[
                'Input 1', 
                {
                  'id': 'ni_17341976077773', 
                  'value': None
                }
              ]], 
              'position': {
                'x': 385.67895362663495, 
                'y': 233.22473246135553
              }, 
              'width': 200, 
              'twoColumn': False, 
              'customClasses': ''
            }], 
            'connections': [
              {
                'id': '17341976120417', 
                'from': 'ni_17341976050491', 
                'to': 'ni_17341976077773'
              }
            ], 
            'panning': {
              'x': 8.137931034482762, 
              'y': 4.349583828775266
            }, 
            'scaling': 0.9344444444444444
          }''', 'javascript')

    if st.button("Создать новую схему"):
        if schema_name and schema_content:
            create_new_schema(schema_name, schema_content)
        else:
            st.error("Необходимо указать имя и содержимое схемы!")

if __name__ == "__main__":
    main()
