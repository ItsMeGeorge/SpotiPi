import datetime


class Output:
    def __init__(self, isDebugging, area_length=15, status_area=7) -> None:
        self.isDebugging = isDebugging

        self.area_length = area_length
        self.status_area = status_area


    def out(self, text, area, status="info"):
        current_time = datetime.datetime.now().strftime("%I:%M")

        if (len(area) <= self.area_length):
            area = area + " "*(self.area_length - len(area))
        else:
            area = area[:len(area) - (len(area) - self.area_length)]

        if (len(status) <= self.status_area):
            status = status + " "*(self.status_area - len(status))
        else:
            status = status[:len(status) - (len(status) - self.status_area)]
        
        print(f"[{current_time}] [{area}] [{status.upper()}] >> {text}")
            
        
        
    def banner(self, *text, area, status="info", min_length=35):
        current_time = datetime.datetime.now().strftime("%I:%M")
        
        if (len(area) <= self.area_length):
            area = area + " "*(self.area_length - len(area))
        else:
            area = area[:len(area) - (len(area) - self.area_length)]

        if (len(status) <= self.status_area):
            status = status + " "*(self.status_area - len(status))
        else:
            status = status[:len(status) - (len(status) - self.status_area)]
        
        # Calculate the maximum length of the lines for proper banner width
        max_length = max(len(line) for line in text)
        max_length = max_length + 4 if max_length > min_length else min_length
        border = "=" * max_length  # Adjust for padding and borders

        print()
        print(f"[{current_time}] [{area}] [{status.upper()}] >>")

        print(border, "\n")
        for line in text:
            print(f"|{line.strip().center(max_length - 2)}|\n")
        print(border)
        print()
        

    def octoPrintProgress(self, area, progress):
        current_time = datetime.datetime.now().strftime("%I:%M")
        
        if (len(area) <= self.area_length):
            area = area + " "*(self.area_length - len(area))
        else:
            area = area[:len(area) - (len(area) - self.area_length)]
        
        print(f"[{current_time}] [{area}] [PROGRES] >> \n")
        
        print("="*22)
        print("|" + ">"*(int((progress * 20) / 100)) + " "*(20 - int(((progress * 20) / 100))) + "|   " + str(progress) + "%")
        print("="*22)


    def debug(self, text, area):
        if (self.get_isDebugging()):
            current_time = datetime.datetime.now().strftime("%I:%M")

            if (len(area) <= self.area_length):
                area = area + " "*(self.area_length - len(area))
            else:
                area = area[:len(area) - (len(area) - self.area_length)]

            print(f"[{current_time}] [{area}] [DEBUG  ] >> {text}")
            
            
    def watchdog_out(self, text, blockPosition=None):
        if (self.get_isDebugging()):
            current_time = datetime.datetime.now().strftime("%I:%M")
            output_text = f"[{current_time}][WatchDog] >> {text}"
            
            if (blockPosition == "start"):
                output_text = f"{'='*60}\n{output_text}"
            elif (blockPosition == "end"):
                output_text = f"{output_text}\n{'='*60}"
            elif (blockPosition == "none"):
                output_text = output_text
            else:
                output_text = f"{'='*60}\n{output_text}\n{'='*60}"

            print(output_text)


    def get_isDebugging(self):
        return self.isDebugging


    def startup(self, version=0):
        print("""
 ____                    __        ____           
/\  _`\                 /\ \__  __/\  _`\   __    
\ \,\L\_\  _____     ___\ \ ,_\/\_\ \ \L\ \/\_\   
 \/_\__ \ /\ '__`\  / __`\ \ \/\/\ \ \ ,__/\/\ \  
   /\ \L\ \ \ \L\ \/\ \L\ \ \ \_\ \ \ \ \/  \ \ \ 
   \ `\____\ \ ,__/\ \____/\ \___\\ \_\ \_\   \ \_\    
    \/_____/\ \ \/  \/___/  \/__/ \/_/\/_/    \/_/
             \ \_\                                
              \/_/

==================================================
            """)
        
        print("Startup Sucsessful")
        print(f"Version: {version}")
        print("")
        print("==================================================")
