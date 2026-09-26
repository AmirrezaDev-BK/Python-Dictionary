"""
Offline Python Dictionary / دیکشنری آفلاین پایتون
Complete offline dictionary with bilingual UI and tip menu.
دیکشنری کامل آفلاین با رابط دو زبانه و منوی راهنما
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
import os

# ============================================
# 1. FIND DICTIONARY FILE / پیدا کردن فایل دیکشنری
# ============================================

def find_dictionary_file():
    """
    Search for dictionary file in multiple locations.
    جستجوی فایل دیکشنری در چندین مکان.
    """
    filename = "pyDICT.txt"
    
    possible_paths = [
        # 1. Next to the Python file (first priority)
        os.path.join(os.path.dirname(os.path.abspath(__file__)), filename),
        # 2. Current working directory
        os.path.join(os.getcwd(), filename),
        # 3. In a "data" subfolder
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", filename),
        # 4. Home directory
        os.path.join(os.path.expanduser("~"), filename),
        # 5. Legacy path (backup)
        r"E:\App\coding project\py DICT\pyDICT.txt",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


# ============================================
# 2. LOAD DICTIONARY DATA / بارگذاری داده دیکشنری
# ============================================

def load_dictionary(file_path):
    """
    Load dictionary from text file with duplicate merging.
    بارگذاری دیکشنری از فایل متنی با ادغام ورودی‌های تکراری.
    """
    dictionary = {}
    
    try:
        if not file_path or not os.path.exists(file_path):
            return {}
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Pattern for: term followed by English and Persian definitions
        pattern = r"([a-zA-Z0-9_`~ ]+)\n\s+English:\s*(.+?)\n\s+فارسی:\s*(.+?)(?=\n\n|\Z)"
        matches = re.findall(pattern, content, re.DOTALL)
        
        if matches:
            for term, eng_def, per_def in matches:
                term = term.strip()
                new_definition = f"🇬🇧 English: {eng_def.strip()}\n🇮🇷 فارسی: {per_def.strip()}"
                
                # ✅ Merge duplicates instead of overwriting
                if term in dictionary:
                    dictionary[term] += "\n\n" + new_definition
                else:
                    dictionary[term] = new_definition
        else:
            # Fallback: Simple format
            pattern = r"([a-zA-Z0-9_`~ ]+):\s*(.+?)(?=\n[a-zA-Z0-9_`~ ]+:|$)"
            matches = re.findall(pattern, content, re.DOTALL)
            for term, definition in matches:
                term = term.strip()
                new_definition = definition.strip().replace("\n", " ")
                if term in dictionary:
                    dictionary[term] += "\n\n" + new_definition
                else:
                    dictionary[term] = new_definition
        
        return dictionary
    
    except Exception as e:
        print(f"[Error] Failed to load dictionary: {e}")
        return {}


# ============================================
# 3. MAIN APPLICATION CLASS / کلاس اصلی برنامه
# ============================================

class DictionaryApp:
    """Main application class / کلاس اصلی برنامه"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📖 Python Dictionary / دیکشنری پایتون")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        
        # Set app icon if available / تنظیم آیکون برنامه
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # ============================================
        # 📍 FILE PATH / مسیر فایل (Relative - قابل حمل)
        # ============================================
        self.file_path = find_dictionary_file()
        
        if self.file_path is None:
            messagebox.showerror(
                "Error / خطا",
                "Dictionary file 'pyDICT.txt' not found!\n"
                "فایل دیکشنری 'pyDICT.txt' پیدا نشد!\n\n"
                "Please place it next to pyDICT.py\n"
                "لطفاً آن را کنار فایل pyDICT.py قرار دهید."
            )
            self.dictionary = {}
        else:
            self.dictionary = load_dictionary(self.file_path)
            if not self.dictionary:
                messagebox.showerror(
                    "Error / خطا",
                    f"File is empty or unreadable:\n{self.file_path}"
                )
        
        self.words = sorted(self.dictionary.keys(), key=str.lower)
        self.total_words = len(self.words)
        
        # UI Language / زبان رابط کاربری
        self.ui_lang = "fa"  # "fa" for Persian, "en" for English
        
        # Language text / متن‌های زبان
        self.lang_text = {
            "fa": {
                "title": "📖 دیکشنری پایتون",
                "subtitle": "مرجع آفلاین پایتون",
                "search_label": "🔍 جستجو:",
                "search_btn": "🔎 جستجو",
                "theme_btn": "🌓 تغییر تم",
                "clear_btn": "🗑️ پاک کردن",
                "status_loaded": "📚 {0} کلمه بارگذاری شد",
                "status_loading": "📚 در حال بارگذاری...",
                "status_found": "🔍 {0} نتیجه یافت شد",
                "status_no_results": "❌ نتیجه‌ای برای '{0}' یافت نشد",
                "status_viewing": "📖 مشاهده: {0}",
                "words_label": "📚 کلمات",
                "definition_label": "📖 تعریف",
                "no_words": "⚠️ هیچ کلمه‌ای بارگذاری نشد!",
                "select_word": "🔍 یک کلمه را از لیست انتخاب کنید یا جستجو کنید!\n\n💡 نکات:\n• برای دیدن تعریف، روی کلمه کلیک کنید\n• برای فیلتر کردن کلمات، در جعبه جستجو تایپ کنید\n• Enter را برای جستجو فشار دهید\n\n📚 تعداد کل کلمات: {0}",
                "word_not_found": "❌ کلمه یافت نشد!\n\n💡 کلمه دیگری را امتحان کنید.",
                "tip_menu": "💡 راهنما",
                "tip_title": "💡 نکات استفاده از دیکشنری",
                "tip_1": "🔍 برای دیدن تعریف، روی هر کلمه در لیست کلیک کنید",
                "tip_2": "📝 برای فیلتر کردن کلمات، در جعبه جستجو تایپ کنید",
                "tip_3": "⌨️ برای جستجو، کلید Enter را فشار دهید",
                "tip_4": "🔤 جستجو به حروف بزرگ و کوچک حساس نیست",
                "tip_5": "🌓 با دکمه Theme، تم تاریک/روشن را تغییر دهید",
                "tip_6": "🌍 زبان رابط کاربری را با دکمه EN/فا تغییر دهید",
                "tip_7": "📊 تعداد کل کلمات: {0}",
                "tip_8": "📖 این یک دیکشنری مرجع آفلاین پایتون است",
                "tip_9": "📂 دیکشنری از فایل متنی بارگذاری می‌شود",
                "tip_close": "بستن",
                "exit": "❌ خروج",
                "refresh": "🔄 بروزرسانی"
            },
            "en": {
                "title": "📖 Python Dictionary",
                "subtitle": "Offline Python Reference",
                "search_label": "🔍 Search:",
                "search_btn": "🔎 Search",
                "theme_btn": "🌓 Toggle Theme",
                "clear_btn": "🗑️ Clear",
                "status_loaded": "📚 {0} words loaded",
                "status_loading": "📚 Loading...",
                "status_found": "🔍 Found {0} results",
                "status_no_results": "❌ No results found for '{0}'",
                "status_viewing": "📖 Viewing: {0}",
                "words_label": "📚 Words",
                "definition_label": "📖 Definition",
                "no_words": "⚠️ No words loaded!",
                "select_word": "🔍 Select a word from the list or search for one!\n\n💡 Tips:\n• Click any word to see its definition\n• Type in the search box to filter words\n• Press Enter to search\n• Search is case-insensitive\n\n📚 Total words: {0}",
                "word_not_found": "❌ Word not found!\n\n💡 Try another word.",
                "tip_menu": "💡 Tips",
                "tip_title": "💡 Tips for using the dictionary",
                "tip_1": "🔍 Click any word in the list to see its definition",
                "tip_2": "📝 Type in the search box to filter words",
                "tip_3": "⌨️ Press Enter to search",
                "tip_4": "🔤 Search is case-insensitive",
                "tip_5": "🌓 Toggle dark/light theme with the Theme button",
                "tip_6": "🌍 Change UI language with EN/فا button",
                "tip_7": "📊 Total words: {0}",
                "tip_8": "📖 This is an offline Python reference dictionary",
                "tip_9": "📂 Dictionary is loaded from a text file",
                "tip_close": "Close",
                "exit": "❌ Exit",
                "refresh": "🔄 Refresh"
            }
        }
        
        # Theme / تم
        self.dark_mode = False
        
        # Colors / رنگ‌ها - Beautiful modern colors
        self.light_colors = {
            'bg': '#f0f4f8',
            'fg': '#1a202c',
            'header_bg': '#2c3e50',
            'header_fg': 'white',
            'entry_bg': 'white',
            'entry_fg': '#1a202c',
            'button_bg': '#4a90e2',
            'button_fg': 'white',
            'result_bg': 'white',
            'result_fg': '#1a202c',
            'list_bg': 'white',
            'list_fg': '#1a202c',
            'highlight': '#4a90e2',
            'status_fg': '#6c7a89',
            'search_frame_bg': '#f0f4f8',
            'accent1': '#4a90e2',
            'accent2': '#e67e22',
            'accent3': '#2ecc71'
        }
        
        self.dark_colors = {
            'bg': '#0d1117',
            'fg': '#e2e8f0',
            'header_bg': '#161b22',
            'header_fg': 'white',
            'entry_bg': '#1e293b',
            'entry_fg': '#e2e8f0',
            'button_bg': '#4a90e2',
            'button_fg': 'white',
            'result_bg': '#1e293b',
            'result_fg': '#e2e8f0',
            'list_bg': '#1e293b',
            'list_fg': '#e2e8f0',
            'highlight': '#4a90e2',
            'status_fg': '#a0aec0',
            'search_frame_bg': '#0d1117',
            'accent1': '#4a90e2',
            'accent2': '#e67e22',
            'accent3': '#2ecc71'
        }
        
        self.colors = self.light_colors.copy()
        
        # Debounce state for search / وضعیت debounce برای جستجو
        self._search_after_id = None
        
        # Setup UI / راه‌اندازی رابط کاربری
        self.setup_ui()
        
        self.show_all_words()
        self.show_default_message()
        
        if self.total_words > 0:
            self.update_status(self.get_text("status_loaded").format(self.total_words))
        else:
            self.update_status(self.get_text("no_words"))
    
    def get_text(self, key):
        """Get text in current UI language / دریافت متن به زبان فعلی"""
        return self.lang_text[self.ui_lang].get(key, key)
    
    # ============================================
    # UI SETUP / راه‌اندازی رابط کاربری
    # ============================================
    
    def setup_ui(self):
        """Setup the user interface / راه‌اندازی رابط کاربری"""
        
        self.root.config(bg=self.colors['bg'])
        
        # ============================================
        # HEADER / سربرگ
        # ============================================
        self.header_frame = tk.Frame(self.root, bg=self.colors['header_bg'], height=80)
        self.header_frame.pack(fill="x", pady=(0, 10))
        self.header_frame.pack_propagate(False)
        
        header_inner = tk.Frame(self.header_frame, bg=self.colors['header_bg'])
        header_inner.pack(expand=True)
        
        self.header_label = tk.Label(
            header_inner,
            text=self.get_text("title"),
            font=("Segoe UI", 22, "bold"),
            bg=self.colors['header_bg'],
            fg=self.colors['header_fg']
        )
        self.header_label.pack()
        
        self.subtitle_label = tk.Label(
            header_inner,
            text=self.get_text("subtitle"),
            font=("Segoe UI", 10),
            bg=self.colors['header_bg'],
            fg="#a0aec0"
        )
        self.subtitle_label.pack()
        
        # ============================================
        # SEARCH BAR / نوار جستجو
        # ============================================
        self.search_frame = tk.Frame(self.root, bg=self.colors['search_frame_bg'])
        self.search_frame.pack(pady=15, padx=25, fill="x")
        
        # Search label
        self.search_label = tk.Label(
            self.search_frame,
            text=self.get_text("search_label"),
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['search_frame_bg'],
            fg=self.colors['fg']
        )
        self.search_label.pack(side="left", padx=(0, 10))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.search_auto_debounced())
        
        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 12),
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            relief="solid",
            bd=2,
            width=35,
            highlightcolor=self.colors['accent1']
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_word())
        self.search_entry.focus()
        
        # Search button
        self.search_btn = tk.Button(
            self.search_frame,
            text=self.get_text("search_btn"),
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['accent1'],
            fg=self.colors['button_fg'],
            padx=25,
            pady=8,
            relief="flat",
            cursor="hand2",
            command=self.search_word
        )
        self.search_btn.pack(side="left", padx=(0, 10))
        
        # Language toggle
        self.lang_btn = tk.Button(
            self.search_frame,
            text="🇮🇷 فا",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['accent2'],
            fg="white",
            padx=12,
            pady=8,
            relief="flat",
            cursor="hand2",
            command=self.toggle_language
        )
        self.lang_btn.pack(side="left", padx=(0, 5))
        
        # Theme toggle
        self.theme_btn = tk.Button(
            self.search_frame,
            text=self.get_text("theme_btn"),
            font=("Segoe UI", 10),
            bg="#6c7a89",
            fg="white",
            padx=12,
            pady=8,
            relief="flat",
            cursor="hand2",
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="left", padx=(0, 5))
        
        # Tip button
        self.tip_btn = tk.Button(
            self.search_frame,
            text=self.get_text("tip_menu"),
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['accent3'],
            fg="white",
            padx=12,
            pady=8,
            relief="flat",
            cursor="hand2",
            command=self.show_tips
        )
        self.tip_btn.pack(side="left")
        
        # ============================================
        # MAIN CONTENT / محتوای اصلی
        # ============================================
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.main_frame.pack(pady=10, padx=25, fill="both", expand=True)
        
        # Left: Word List / لیست کلمات
        self.list_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        self.list_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.list_label = tk.Label(
            self.list_frame,
            text=self.get_text("words_label"),
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.list_label.pack(anchor="w", pady=(0, 5))
        
        self.list_container = tk.Frame(self.list_frame, bg=self.colors['bg'])
        self.list_container.pack(fill="both", expand=True)
        
        self.word_listbox = tk.Listbox(
            self.list_container,
            font=("Segoe UI", 11),
            bg=self.colors['list_bg'],
            fg=self.colors['list_fg'],
            selectbackground=self.colors['highlight'],
            selectforeground="white",
            relief="solid",
            bd=2,
            activestyle="none"
        )
        self.word_listbox.pack(side="left", fill="both", expand=True)
        self.word_listbox.bind("<<ListboxSelect>>", self.on_word_select)
        
        self.list_scrollbar = ttk.Scrollbar(self.list_container, orient="vertical", command=self.word_listbox.yview)
        self.list_scrollbar.pack(side="right", fill="y")
        self.word_listbox.config(yscrollcommand=self.list_scrollbar.set)
        
        # Right: Result / نتیجه
        self.result_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        self.result_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.result_label = tk.Label(
            self.result_frame,
            text=self.get_text("definition_label"),
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.result_label.pack(anchor="w", pady=(0, 5))
        
        self.result_text = tk.Text(
            self.result_frame,
            font=("Segoe UI", 11),
            bg=self.colors['result_bg'],
            fg=self.colors['result_fg'],
            wrap="word",
            padx=20,
            pady=20,
            relief="solid",
            bd=2,
            state="disabled"
        )
        self.result_text.pack(fill="both", expand=True)
        
        self.result_scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.result_text.yview)
        self.result_scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=self.result_scrollbar.set)
        
        # ============================================
        # STATUS BAR / نوار وضعیت
        # ============================================
        self.status_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.status_frame.pack(fill="x", padx=25, pady=(5, 10))
        
        self.status_label = tk.Label(
            self.status_frame,
            text=self.get_text("status_loading"),
            font=("Segoe UI", 10),
            bg=self.colors['bg'],
            fg=self.colors['status_fg'],
            anchor="w"
        )
        self.status_label.pack(side="left")
        
        self.clear_btn = tk.Button(
            self.status_frame,
            text=self.get_text("clear_btn"),
            font=("Segoe UI", 10),
            bg=self.colors['accent2'],
            fg="white",
            padx=15,
            pady=5,
            relief="flat",
            cursor="hand2",
            command=self.clear_result
        )
        self.clear_btn.pack(side="right")
    
    # ============================================
    # UI FUNCTIONS / توابع رابط کاربری
    # ============================================
    
    def toggle_language(self):
        """Toggle between Persian and English UI / تغییر بین زبان فارسی و انگلیسی"""
        if self.ui_lang == "fa":
            self.ui_lang = "en"
            self.lang_btn.config(text="🇮🇷 فا")
        else:
            self.ui_lang = "fa"
            self.lang_btn.config(text="🇬🇧 EN")
        
        self.update_ui_text()
        self.show_default_message()
        self.update_status(self.get_text("status_loaded").format(self.total_words))
    
    def update_ui_text(self):
        """Update all UI text / به‌روزرسانی همه متن‌های رابط کاربری"""
        self.header_label.config(text=self.get_text("title"))
        self.subtitle_label.config(text=self.get_text("subtitle"))
        self.search_label.config(text=self.get_text("search_label"))
        self.search_btn.config(text=self.get_text("search_btn"))
        self.theme_btn.config(text=self.get_text("theme_btn"))
        self.clear_btn.config(text=self.get_text("clear_btn"))
        self.tip_btn.config(text=self.get_text("tip_menu"))
        self.list_label.config(text=self.get_text("words_label"))
        self.result_label.config(text=self.get_text("definition_label"))
    
    def show_tips(self):
        """Show tips dialog / نمایش کادر راهنما"""
        tips_text = f"""
╔══════════════════════════════════════════════════════════════╗
║              {self.get_text("tip_title")}              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  {self.get_text("tip_1")}                                     ║
║  {self.get_text("tip_2")}                                     ║
║  {self.get_text("tip_3")}                                     ║
║  {self.get_text("tip_4")}                                     ║
║  {self.get_text("tip_5")}                                     ║
║  {self.get_text("tip_6")}                                     ║
║  {self.get_text("tip_7").format(self.total_words)}            ║
║  {self.get_text("tip_8")}                                     ║
║  {self.get_text("tip_9")}                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        messagebox.showinfo(
            self.get_text("tip_menu"),
            tips_text
        )
    
    # ============================================
    # CORE FUNCTIONS / توابع اصلی
    # ============================================
    
    def show_all_words(self):
        """Show all words in the list / نمایش همه کلمات در لیست"""
        self.word_listbox.delete(0, tk.END)
        for word in self.words:
            self.word_listbox.insert(tk.END, word)
    
    def show_filtered_words(self, query):
        """Show filtered words / نمایش کلمات فیلتر شده"""
        self.word_listbox.delete(0, tk.END)
        query = query.lower().strip()
        if not query:
            self.show_all_words()
            return
        
        for word in self.words:
            if query in word.lower():
                self.word_listbox.insert(tk.END, word)
    
    def display_definition(self, word):
        """Display definition of a word / نمایش تعریف یک کلمه"""
        if word not in self.dictionary:
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", self.get_text("word_not_found"))
            self.result_text.config(state="disabled")
            return
        
        definition = self.dictionary[word]
        display_text = f"📖 {word}\n"
        display_text += "═" * 50 + "\n\n"
        display_text += definition + "\n\n"
        display_text += "─" * 50 + "\n"
        display_text += f"📚 Python Official Glossary / واژه‌نامه رسمی پایتون"
        
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", display_text)
        
        # ✅ RTL alignment for Persian text
        self.result_text.tag_configure("rtl", justify="right")
        self.result_text.config(state="disabled")
        
        try:
            items = self.word_listbox.get(0, tk.END)
            if word in items:
                index = items.index(word)
                self.word_listbox.selection_clear(0, tk.END)
                self.word_listbox.selection_set(index)
                self.word_listbox.see(index)
        except ValueError:
            pass
    
    def show_default_message(self):
        """Show default message / نمایش پیام پیش‌فرض"""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", self.get_text("select_word").format(self.total_words))
        self.result_text.config(state="disabled")
    
    def clear_result(self):
        """Clear search and result / پاک کردن جستجو و نتیجه"""
        self.search_var.set("")
        self.show_all_words()
        self.show_default_message()
        self.update_status(self.get_text("status_loaded").format(self.total_words))
    
    def update_status(self, message):
        """Update status bar / به‌روزرسانی نوار وضعیت"""
        self.status_label.config(text=message)
    
    # ============================================
    # SEARCH FUNCTIONS / توابع جستجو
    # ============================================
    
    def search_auto_debounced(self):
        """Debounced search - waits 150ms after typing stops / جستجوی تاخیری"""
        if self._search_after_id is not None:
            self.root.after_cancel(self._search_after_id)
        self._search_after_id = self.root.after(150, self.search_auto)
    
    def search_auto(self):
        """Auto-complete search / جستجوی خودکار"""
        self._search_after_id = None
        query = self.search_var.get()
        self.show_filtered_words(query)
        
        if query:
            self.update_status(self.get_text("status_found").format(self.word_listbox.size()))
        else:
            self.update_status(self.get_text("status_loaded").format(self.total_words))
    
    def search_word(self):
        """Search for a specific word / جستجوی یک کلمه خاص"""
        query = self.search_var.get().strip()
        if not query:
            self.show_all_words()
            self.show_default_message()
            return
        
        # Find exact match (case-insensitive)
        matching_words = [w for w in self.dictionary.keys() if w.lower() == query.lower()]
        
        if matching_words:
            self.display_definition(matching_words[0])
            self.show_filtered_words(query)
            self.update_status(self.get_text("status_viewing").format(matching_words[0]))
            return
        
        # Find partial matches
        matches = [w for w in self.words if query.lower() in w.lower()]
        if matches:
            self.show_filtered_words(query)
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", f"🔍 Results for '{query}':\n\n" + "\n".join([f"• {w}" for w in matches[:20]]))
            self.result_text.config(state="disabled")
            self.update_status(self.get_text("status_found").format(len(matches)))
        else:
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", self.get_text("status_no_results").format(query))
            self.result_text.config(state="disabled")
            self.update_status(self.get_text("status_no_results").format(query))
    
    def on_word_select(self, event):
        """Handle word selection from list / مدیریت انتخاب کلمه از لیست"""
        selection = self.word_listbox.curselection()
        if selection:
            word = self.word_listbox.get(selection[0])
            self.display_definition(word)
            self.search_var.set(word)
            self.update_status(self.get_text("status_viewing").format(word))
    
    # ============================================
    # THEME TOGGLE / تغییر تم
    # ============================================
    
    def toggle_theme(self):
        """Toggle between light and dark theme / تغییر بین تم روشن و تاریک"""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            self.colors = self.dark_colors.copy()
        else:
            self.colors = self.light_colors.copy()
        
        # Apply colors
        self.root.config(bg=self.colors['bg'])
        self.header_frame.config(bg=self.colors['header_bg'])
        self.header_label.config(bg=self.colors['header_bg'], fg=self.colors['header_fg'])
        self.subtitle_label.config(bg=self.colors['header_bg'], fg="#a0aec0")
        
        self.search_frame.config(bg=self.colors['search_frame_bg'])
        for child in self.search_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=self.colors['search_frame_bg'], fg=self.colors['fg'])
            elif isinstance(child, tk.Entry):
                child.config(bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        
        self.main_frame.config(bg=self.colors['bg'])
        self.list_frame.config(bg=self.colors['bg'])
        self.list_container.config(bg=self.colors['bg'])
        self.list_label.config(bg=self.colors['bg'], fg=self.colors['fg'])
        self.word_listbox.config(bg=self.colors['list_bg'], fg=self.colors['list_fg'])
        
        self.result_frame.config(bg=self.colors['bg'])
        self.result_label.config(bg=self.colors['bg'], fg=self.colors['fg'])
        self.result_text.config(bg=self.colors['result_bg'], fg=self.colors['result_fg'])
        
        self.status_frame.config(bg=self.colors['bg'])
        self.status_label.config(bg=self.colors['bg'], fg=self.colors['status_fg'])
        
        # Refresh display
        selection = self.word_listbox.curselection()
        if selection:
            word = self.word_listbox.get(selection[0])
            self.display_definition(word)
        else:
            self.show_default_message()


# ============================================
# 4. RUN APPLICATION / اجرای برنامه
# ============================================

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()