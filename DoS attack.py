import requests
import concurrent.futures
import time
import random
from user_agents import user_agents
from urllib.parse import urlparse
import sys

# ألوان ANSI للتنسيق
R = '\033[1;31m'  # أحمر
X = '\033[1;33m'  # أصفر
F = '\033[2;32m'  # أخضر
C = "\033[1;97m"  # أبيض
B = '\033[2;36m'  # سمائي
Y = '\033[1;34m'  # أزرق فاتح
P = '\033[1;35m'  # بنفسجي
M = '\033[1;91m'  # أحمر فاتح
RESET = '\033[0m'  # إعادة الضبط

# إعدادات التحكم
MAX_RETRIES = 3
REQUEST_TIMEOUT = 15
COOLDOWN_PERIOD = 2
MAX_THREADS = 20000
MAX_REQUESTS = 100000

class ABDELAZIZ_StressTester:
    def __init__(self):
        self.target_url = ""
        self.session = requests.Session()
        self.session.headers.update({
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br'
        })
        self.total_tests = 0
        self.total_success = 0
        self.request_types = ["GET", "POST"]  # الإفتراضي: كلا النوعين
    
    def clear_screen(self):
        """مسح الشاشة"""
        print('\033[H\033[J', end='')
    
    def print_banner(self):
        """شعار ABDELAZIZ المميز"""
        self.clear_screen()
        print(f"\n{M}╔══════════════════════════════════════════════════════════╗")
        print(f"║ {C}   █████╗ ██████╗ ██████╗ ███████╗ █████╗ ███████╗ ██╗ ███████╗ {M}║")
        print(f"║ {C}  ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗╚══███╔╝██║██╔════╝ {M}║")
        print(f"║ {C}  ███████║██████╔╝██║  ██║█████╗  ███████║  ███╔╝ ██║███████╗ {M}║")
        print(f"║ {C}  ██╔══██║██╔══██╗██║  ██║██╔══╝  ██╔══██║ ███╔╝  ██║╚════██║ {M}║")
        print(f"║ {C}  ██║  ██║██████╔╝██████╔╝███████╗██║  ██║███████╗██║███████║ {M}║")
        print(f"║ {C}  ╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝ {M}║")
        print(f"╠══════════════════════════════════════════════════════════╣")
        print(f"║ {B}         أداة اختبار الضغط المتقدمة (v3.2)         {M}║")
        print(f"║ {B}    إصدار متخصص لاختبار صفحات تسجيل الدخول         {M}║")
        print(f"║ {B}             تم التطوير بواسطة ABDELAZIZ            {M}║")
        print(f"╚══════════════════════════════════════════════════════════╝{RESET}")
    
    def get_target_url(self):
        """الحصول على عنوان URL من المستخدم"""
        print(f"\n{Y}[{C}*{Y}]{C} يرجى إدخال عنوان URL المستهدف (مثال: https://example.com/login)")
        print(f"{Y}[{C}*{Y}]{C} تأكد من أن الرابط يبدأ بـ {F}http:// {C}أو {F}https://{RESET}")
        
        while True:
            url = input(f"\n{Y}[{C}?{Y}]{C} أدخل URL: {B}").strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            if self.validate_url(url):
                self.target_url = url
                print(f"{Y}[{F}✓{Y}]{C} تم تعيين الهدف: {B}{self.target_url}{RESET}")
                return True
            
            print(f"{Y}[{R}!{Y}]{C} عنوان URL غير صالح أو لا يمكن الوصول إليه! يرجى المحاولة مرة أخرى.{RESET}")
    
    def validate_url(self, url):
        """التحقق من صحة URL (نسخة معدلة لتقبل أي موقع موجود)"""
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return False
            
            # إرسال طلب HEAD مع التعامل مع جميع الأخطاء
            try:
                test = requests.head(
                    url, 
                    timeout=5, 
                    allow_redirects=True,
                    headers={'User-Agent': random.choice(user_agents)}
                )
                # نعتبر الرابط صالحاً إذا وصلنا للخادم (حتى لو أعاد 404/403/500)
                return True
            except requests.exceptions.SSLError:
                # حاول مع http إذا فشل https
                if url.startswith('https://'):
                    http_url = url.replace('https://', 'http://')
                    try:
                        test = requests.head(
                            http_url, 
                            timeout=5,
                            allow_redirects=True,
                            headers={'User-Agent': random.choice(user_agents)}
                        )
                        self.target_url = http_url  # تحديث الرابط لاستخدام http بدلاً من https
                        return True
                    except:
                        return False
                return False
            except:
                return False
        except:
            return False
    
    def generate_login_data(self):
        """إنشاء بيانات تسجيل دخول وهمية"""
        users = ['admin', 'user', 'test', 'guest', 'root']
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com']
        return {
            "username": random.choice(users) + str(random.randint(1, 1000)),
            "password": f"P@ssw0rd{random.randint(100, 999)}",
            "email": f"{random.choice(users)}{random.randint(1, 1000)}@{random.choice(domains)}",
            "csrf_token": f"csrf_{random.getrandbits(192):048x}",
            "remember_me": random.choice(["true", "false", "1", "0"])
        }
    
    def set_request_types(self):
        """تحديد أنواع الطلبات المطلوبة"""
        print(f"\n{Y}[{C}*{Y}]{C} اختر نوع الطلبات:")
        print(f"{Y}[{C}1{Y}]{C} GET فقط")
        print(f"{Y}[{C}2{Y}]{C} POST فقط")
        print(f"{Y}[{C}3{Y}]{C} GET و POST معاً (افتراضي)")
        
        choice = input(f"\n{Y}[{C}?{Y}]{C} اختر الخيار (1-3): {B}").strip()
        
        if choice == "1":
            self.request_types = ["GET"]
            print(f"{Y}[{F}✓{Y}]{C} سيتم إرسال طلبات GET فقط{RESET}")
        elif choice == "2":
            self.request_types = ["POST"]
            print(f"{Y}[{F}✓{Y}]{C} سيتم إرسال طلبات POST فقط{RESET}")
        else:
            self.request_types = ["GET", "POST"]
            print(f"{Y}[{F}✓{Y}]{C} سيتم إرسال طلبات GET و POST معاً{RESET}")
    
    def send_advanced_request(self, user_agent):
        """إرسال طلب HTTP متقدم"""
        method = random.choice(self.request_types)
        
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": random.choice([self.target_url, "https://google.com", "https://bing.com"]),
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Request-ID": f"req_{random.getrandbits(128):032x}",
            "Cache-Control": "no-cache"
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                if method == "GET":
                    response = self.session.get(
                        self.target_url, 
                        headers=headers, 
                        timeout=REQUEST_TIMEOUT,
                        allow_redirects=True
                    )
                elif method == "POST":
                    headers.update({
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-Requested-With": "XMLHttpRequest"
                    })
                    response = self.session.post(
                        self.target_url,
                        headers=headers,
                        data=self.generate_login_data(),
                        timeout=REQUEST_TIMEOUT
                    )
                
                return {
                    "method": method,
                    "status": response.status_code,
                    "time": response.elapsed.total_seconds(),
                    "success": response.ok,
                    "size": len(response.content) if hasattr(response, 'content') else 0,
                    "redirect": len(response.history) > 0
                }
                
            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    return {
                        "method": method,
                        "status": str(e),
                        "time": 0,
                        "success": False,
                        "size": 0,
                        "redirect": False
                    }
                time.sleep(0.2)
    
    def analyze_results(self, results):
        """تحليل النتائج بشكل متقدم"""
        stats = {
            "status_codes": {},
            "methods": {},
            "success": 0,
            "redirects": 0,
            "total_time": 0,
            "total_size": 0,
            "response_times": [],
            "errors": 0
        }
        
        for result in results:
            status = str(result.get('status', 'UNKNOWN'))
            method = result.get('method', 'UNKNOWN')
            
            # تجميع الإحصائيات
            stats["status_codes"][status] = stats["status_codes"].get(status, 0) + 1
            stats["methods"][method] = stats["methods"].get(method, 0) + 1
            
            if result.get('success', False):
                stats["success"] += 1
                stats["total_time"] += result.get('time', 0)
                stats["response_times"].append(result.get('time', 0))
                
                if result.get('redirect', False):
                    stats["redirects"] += 1
            else:
                stats["errors"] += 1
            
            stats["total_size"] += result.get('size', 0)
        
        # حساب المتوسطات والنسب
        stats["avg_time"] = stats["total_time"] / max(1, stats["success"])
        stats["avg_size"] = stats["total_size"] / max(1, len(results))
        stats["success_rate"] = (stats["success"] / len(results)) * 100
        stats["error_rate"] = (stats["errors"] / len(results)) * 100
        
        # حساب percentiles لزمن الاستجابة
        stats["response_times"].sort()
        if stats["response_times"]:
            stats["p90"] = stats["response_times"][int(len(stats["response_times"]) * 0.90)]
            stats["p95"] = stats["response_times"][int(len(stats["response_times"]) * 0.95)]
            stats["p99"] = stats["response_times"][int(len(stats["response_times"]) * 0.99)]
        else:
            stats["p90"] = stats["p95"] = stats["p99"] = 0
            
        return stats
    
    def print_results(self, stats, concurrent_users, total_requests, duration):
        """عرض النتائج بتنسيق متقدم"""
        success_color = F if stats["success_rate"] > 75 else X if stats["success_rate"] > 40 else R
        
        print(f"\n{Y}╔══════════════════════════════════════════════════════════╗")
        print(f"║ {C}                 نتائج اختبار الضغط                 {Y}║")
        print(f"╠══════════════════════════════════════════════════════════╣")
        print(f"║ {C}الهدف:{B} {self.target_url[:45]}{'...' if len(self.target_url) > 45 else ''}{Y} ║")
        print(f"╠══════════════════════════════════════════════════════════╣")
        print(f"║ {C}المستخدمون: {Y}{concurrent_users:<8}{C} الطلبات: {Y}{total_requests:<8}{C} المدة: {Y}{duration:.2f} ثانية{Y}║")
        print(f"║ {C}معدل النجاح: {success_color}{stats['success_rate']:.1f}%{C}   معدل الخطأ: {R}{stats['error_rate']:.1f}%{Y}          ║")
        print(f"║ {C}إعادة التوجيه: {Y}{stats['redirects']}{C}   متوسط الزمن: {Y}{stats['avg_time']:.3f} ثانية{Y}          ║")
        print(f"║ {C}P90: {Y}{stats['p90']:.3f}{C} ثانية   P95: {Y}{stats['p95']:.3f}{C} ثانية   P99: {Y}{stats['p99']:.3f} ثانية{Y}║")
        print(f"║ {C}معدل الطلبات: {Y}{total_requests/max(0.1, duration):.1f}/ثانية{C} الحجم: {Y}{stats['total_size']/1024:.2f} ك.ب{Y}║")
        print(f"╠══════════════════════════════════════════════════════════╣")
        print(f"║ {C}الطرق المستخدمة:                                    {Y}║")
        
        for method, count in sorted(stats["methods"].items(), key=lambda x: x[1], reverse=True):
            print(f"║  {C}{method}: {Y}{count:<6}{C} ({count/total_requests:.1%}){Y}                      ║")
        
        print(f"╠══════════════════════════════════════════════════════════╣")
        print(f"║ {C}رموز الحالة:                                         {Y}║")
        
        for status, count in sorted(stats["status_codes"].items(), key=lambda x: x[1], reverse=True)[:10]:
            color = F if status.startswith(('2', '3')) else X if status.startswith('1') else R
            print(f"║  {color}{status[:20]:<20}{Y}{count:<6}{C} ({count/total_requests:.1%}){Y}          ║")
        
        print(f"╚══════════════════════════════════════════════════════════╝{RESET}")
    
    def get_test_parameters(self):
        """الحصول على معايير الاختبار من المستخدم"""
        print(f"\n{Y}[{C}*{Y}]{C} يرجى إدخال معايير اختبار الضغط")
        
        while True:
            try:
                concurrent_users = int(input(f"{Y}[{C}?{Y}]{C} عدد المستخدمين المتزامنين (1-{MAX_THREADS}): {B}"))
                if 1 <= concurrent_users <= MAX_THREADS:
                    break
                print(f"{Y}[{R}!{Y}]{C} الرقم يجب أن يكون بين 1 و {MAX_THREADS}{RESET}")
            except ValueError:
                print(f"{Y}[{R}!{Y}]{C} يرجى إدخال رقم صحيح{RESET}")
        
        while True:
            try:
                total_requests = int(input(f"{Y}[{C}?{Y}]{C} إجمالي عدد الطلبات (1-{MAX_REQUESTS}): {B}"))
                if 1 <= total_requests <= MAX_REQUESTS:
                    break
                print(f"{Y}[{R}!{Y}]{C} الرقم يجب أن يكون بين 1 و {MAX_REQUESTS}{RESET}")
            except ValueError:
                print(f"{Y}[{R}!{Y}]{C} يرجى إدخال رقم صحيح{RESET}")
        
        return concurrent_users, total_requests
    
    def show_progress(self, completed, total, start_time):
        """عرض شريط التقدم"""
        elapsed = time.time() - start_time
        percent = completed / total
        bar_length = 40
        filled_length = int(bar_length * percent)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        rps = completed / max(0.1, elapsed)
        eta = (total - completed) / max(0.1, rps)
        
        sys.stdout.write(
            f"\r{Y}[{C}*{Y}]{C} {bar} {percent:.1%} | "
            f"مكتمل: {Y}{completed}{C}/{Y}{total}{C} | "
            f"السرعة: {Y}{rps:.1f} طلب/ث{C} | "
            f"الوقت المتبقي: {Y}{eta:.1f} ثانية{RESET}"
        )
        sys.stdout.flush()
    
    def run_stress_test(self, concurrent_users, total_requests):
        """تنفيذ اختبار الضغط"""
        start_time = time.time()
        results = []
        
        try:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=min(concurrent_users, MAX_THREADS)
            ) as executor:
                futures = [
                    executor.submit(
                        self.send_advanced_request,
                        random.choice(user_agents)
                    ) for _ in range(total_requests)
                ]
                
                completed = 0
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
                    completed += 1
                    
                    if completed % 10 == 0 or completed == total_requests:
                        self.show_progress(completed, total_requests, start_time)
        
        except KeyboardInterrupt:
            print(f"\n{Y}[{R}!{Y}]{C} تم إيقاف الاختبار بواسطة المستخدم{RESET}")
            return None, 0
        
        duration = time.time() - start_time
        return results, duration
    
    def run_test(self):
        """الدالة الرئيسية لتشغيل الاختبار"""
        self.print_banner()
        
        if not self.get_target_url():
            return
        
        self.set_request_types()  # اختيار نوع الطلبات
        
        while True:
            concurrent_users, total_requests = self.get_test_parameters()
            
            print(f"\n{Y}[{C}*{Y}]{F} جاري بدء اختبار الضغط...{RESET}")
            print(f"{Y}[{C}*{Y}]{C} المستخدمون المتزامنون: {Y}{concurrent_users}{RESET}")
            print(f"{Y}[{C}*{Y}]{C} إجمالي الطلبات: {Y}{total_requests}{RESET}")
            print(f"{Y}[{C}*{Y}]{C} أنواع الطلبات: {Y}{', '.join(self.request_types)}{RESET}")
            
            results, duration = self.run_stress_test(concurrent_users, total_requests)
            
            if results is None:  # تم إيقاف الاختبار
                break
                
            stats = self.analyze_results(results)
            self.print_results(stats, concurrent_users, total_requests, duration)
            
            # تحديث الإحصائيات الكلية
            self.total_tests += total_requests
            self.total_success += stats["success"]
            
            choice = input(f"\n{Y}[{C}?{Y}]{C} هل تريد إجراء اختبار آخر؟ (نعم/لا): {B}").strip().lower()
            if choice not in ['نعم', 'ن', 'yes', 'y']:
                break
    
    def print_summary(self):
        """عرض ملخص عام بعد الانتهاء"""
        if self.total_tests > 0:
            success_rate = (self.total_success / self.total_tests) * 100
            print(f"\n{Y}╔══════════════════════════════════════════════════════════╗")
            print(f"║ {C}                 ملخص الاختبارات                   {Y}║")
            print(f"╠══════════════════════════════════════════════════════════╣")
            print(f"║ {C}إجمالي الاختبارات: {Y}{self.total_tests}{C}          النجاح: {Y}{self.total_success} ({success_rate:.1f}%){Y}║")
            print(f"╚══════════════════════════════════════════════════════════╝{RESET}")

def main():
    try:
        tester = ABDELAZIZ_StressTester()
        tester.run_test()
        tester.print_summary()
    except Exception as e:
        print(f"\n{R}حدث خطأ غير متوقع: {str(e)}{RESET}")
    finally:
        print(f"\n{Y}[{C}*{Y}]{C} شكراً لاستخدام أداة ABDELAZIZ لاختبار الضغط{RESET}")

if __name__ == "__main__":
    main()