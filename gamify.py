def initialize():

    global cur_hedons, cur_health

    global cur_star, cur_star_activity, star_offer_time

    global cur_time
    global last_activity, run_time
    global last_run, last_lift
    
    global test
    global stars_offered, bored_with_stars, first_star, second_star
    
    cur_hedons = 0
    cur_health = 0
    
    cur_star = None
    cur_star_activity = None
    star_offer_time = None

    stars_offered = 0
    first_star = None
    second_star = None
    bored_with_stars = False
    
    last_activity = None

    last_run = 0
    last_lift = 0
    run_time = 0    

    cur_time = 0
    
    test = False
              

def star_can_be_taken(activity):

    if star_offer_time != cur_time:
        return False
    elif bored_with_stars:
        return False
    elif cur_star != activity:
        return False
    else:
        return True

def perform_activity(activity, duration):
    if activity == "running" or activity == "textbooks" or activity == "resting":
        global cur_health, cur_hedons
        global cur_time
        global last_activity, run_time
        global last_run, last_lift

        star = star_can_be_taken (activity)
        tired = False
        if (cur_time) != 0:
            if (cur_time - last_run < 120) or (cur_time - last_lift < 120):
                tired = True
        if not test:
            cur_time += duration

        if activity == "running":
            # Health
            if test:
                cur_health += 0
            elif not test:
                temp = run_time
                run_time += duration
                if 0 < run_time <= 180:  
                    cur_health += 3*duration

                elif temp > 180:
                    cur_health += duration

                elif run_time >= 180 and temp <= 180:
                    cur_health += 3*(180-temp) + (run_time-180)

                else:
                    cur_health += 540 + (duration-180)

            # Hedons
            if tired:
                cur_hedons += -2*duration
            else:
                if duration <= 10:
                    cur_hedons += 2*duration
                else:
                    cur_hedons += 20 - 2*(duration-10)

            if star:
                if duration <= 10:
                    cur_hedons += 3*duration
                else:
                    cur_hedons += 30

            # Misc
            if not test:
                last_run = cur_time
                
        elif activity == "textbooks":
            if not test:
                run_time = 0
            # Health
            cur_health += 2*duration

            # Hedons
            if tired:
                cur_hedons += -2*duration
            else:
                if duration <= 20:
                    cur_hedons += 1*duration
                else:
                    cur_hedons += 20 - 1*(duration-20)

            if star:
                if duration <= 10:
                    cur_hedons += 3*duration
                else:
                    cur_hedons += 30
            # Misc
            if not test:
                last_lift = cur_time

        elif activity == "resting":
            if not test:
                run_time = 0

        if not test:
            last_activity = activity

def get_cur_hedons():

    return cur_hedons
    
def get_cur_health():

    return cur_health
    
def offer_star(activity):

    global cur_star, star_offer_time
    global stars_offered, bored_with_stars, first_star, second_star

    cur_star = activity
    star_offer_time = cur_time
    stars_offered += 1

    if stars_offered == 1:
        first_star = star_offer_time
    
    elif stars_offered == 2:
        second_star = star_offer_time

    if cur_time - first_star >= 120:
        stars_offered = 1
        first_star = second_star

    if stars_offered >= 3:
        bored_with_stars = True
        
def most_fun_activity_minute():

    global cur_hedons, cur_health, test
    test = True
    x = cur_hedons
    y = cur_health
    activities = ["running", "textbooks", "resting"]
    headons_min = []
    for activity in activities:
        perform_activity (activity, 1)
        headons_min.append (cur_hedons - x)
        cur_hedons = x
        cur_health = y
    test = False

    if max (headons_min) == headons_min[0]:
        return "running"
    elif max (headons_min) == headons_min[1]:
        return "textbooks"
    else:
        return "resting"

        
if __name__ == '__main__':
    initialize ()

    # Test 1
    """
    offer_star ("running")                  
    perform_activity ("running", 5)
    print (f"Health: {get_cur_health()}")   # 15
    print (f"Headons: {get_cur_hedons()}")  # 25
    offer_star ("running")                  
    perform_activity ("running", 5)     
    print (f"Health: {get_cur_health()}")   # 30
    print (f"Headons: {get_cur_hedons()}")  # 30
    offer_star ("running")                  
    perform_activity ("running", 5)     
    print (f"Health: {get_cur_health()}")   # 45
    print (f"Headons: {get_cur_hedons()}")  # 20
    offer_star ("running")                  
    perform_activity ("running", 120)  
    print (f"Health: {get_cur_health()}")   # 405
    print (f"Headons: {get_cur_hedons()}")  # -220
    offer_star ("running")                  
    perform_activity ("running", 60)   
    print (f"Health: {get_cur_health()}")   # 555
    print (f"Headons: {get_cur_hedons()}")  # -340
    offer_star ("running")                  
    perform_activity ("running", 30) 
    print (f"Health: {get_cur_health()}")   # 585
    print (f"Headons: {get_cur_hedons()}")  # -400
    offer_star ("running")                  
    perform_activity ("running", 30)        
    print (f"Health: {get_cur_health()}")   # 615
    print (f"Headons: {get_cur_hedons()}")  # -460
    """
    # Test 2
    """
    offer_star ("running")            
    perform_activity ("running", 30)  
    print (f"Health: {get_cur_health()}")   # 90
    print (f"Headons: {get_cur_hedons()}")  # 10
    offer_star ("textbooks")           
    perform_activity ("textbooks", 30) 
    print (f"Health: {get_cur_health()}")   # 150
    print (f"Headons: {get_cur_hedons()}")  # -20
    perform_activity ("running", 60)    
    print (f"Health: {get_cur_health()}")   # 330
    print (f"Headons: {get_cur_hedons()}")  # -140
    offer_star ("textbooks")           
    perform_activity ("running", 60)   
    print (f"Health: {get_cur_health()}")   # 510
    print (f"Headons: {get_cur_hedons()}")  # -260
    offer_star ("running")             
    perform_activity ("resting", 60)   
    print (f"Health: {get_cur_health()}")   # -260
    print (f"Headons: {get_cur_hedons()}")  # 510
    offer_star ("textbooks")            
    perform_activity ("textbooks", 30)  
    print (f"Health: {get_cur_health()}")   # 570
    print (f"Headons: {get_cur_hedons()}")  # -290
    offer_star ("running")                  
    perform_activity ("running", 30)    
    print (f"Health: {get_cur_health()}")   # 660
    print (f"Headons: {get_cur_hedons()}")  # -350
    perform_activity ("resting", 120)   
    print (f"Health: {get_cur_health()}")   # 660
    print (f"Headons: {get_cur_hedons()}")  # -350
    offer_star ("textbooks")                
    perform_activity ("textbooks", 30)
    print (f"Health: {get_cur_health()}")   # 720
    print (f"Headons: {get_cur_hedons()}")  # -340
    """