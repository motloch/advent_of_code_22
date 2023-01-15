import re
blueprints = open('19.txt', 'r').read().splitlines()

quality_levels_sum = 0

def process_blueprint(costs, time_available):
    """
    Returns the maximal number of geodes we can crack with given array of costs, if we
    have so much time available.
    """

    # price of converting ore (o) into ore bot, ...
    o_to_o, o_to_c, o_to_obs, c_to_obs, o_to_g, obs_to_g = costs

    def get_max_num_geodes(time_left, ore, clay, obsidian, geodes, o_bots, c_bots, obs_bots, g_bots):
        """
        How much geodes we can maximally open if we are in a given state (time / resources
        / bots)?
        """
        
        # how many geodes we can collect for each of the possible choices of which robot
        # to build next
        res = []

        # we can choose to build no more robots
        res = [geodes + g_bots * time_left]
        
        # check if we can make a geo bot
        if obs_bots > 0:
            
            # how many more resources we need
            o_need = o_to_g - ore
            obs_need = obs_to_g - obsidian

            # how long to collect them
            dtime1 = o_need // o_bots + (1 if o_need % o_bots else 0)
            dtime2 = obs_need // obs_bots + (1 if obs_need % obs_bots else 0)
            dtime = max(dtime1, dtime2, 0)

            # we have enought time left? if so, use recursion
            if dtime < time_left: 
                res.append(get_max_num_geodes(time_left - dtime - 1,
                                                ore      + (dtime + 1)*o_bots - o_to_g,
                                                clay     + (dtime + 1)*c_bots,
                                                obsidian + (dtime + 1)*obs_bots - obs_to_g,
                                                geodes   + (dtime + 1)*g_bots,
                                                o_bots,
                                                c_bots,
                                                obs_bots,
                                                g_bots + 1))

                # if we can make a geo bot now, make it!
                if dtime == 0:
                    return max(res)

        # if it makes sense, try making ore bot as the next one
        # [there is no point having more ore bots than the amount of ore we can consume
        # per round making bots]
        if o_bots < max(o_to_o, o_to_c, o_to_obs, o_to_g):
            o_need = o_to_o - ore
            dtime = o_need // o_bots + (1 if o_need % o_bots else 0)
            dtime = max(0, dtime)

            if dtime < time_left: 
                res.append(get_max_num_geodes(time_left - dtime - 1,
                                                ore      + (dtime + 1)*o_bots - o_to_o,
                                                clay     + (dtime + 1)*c_bots,
                                                obsidian + (dtime + 1)*obs_bots,
                                                geodes   + (dtime + 1)*g_bots,
                                                o_bots   + 1,
                                                c_bots,
                                                obs_bots,
                                                g_bots))

        # if it makes sense, try making one clay bot
        if c_bots < c_to_obs:
            o_need = o_to_c - ore
            dtime = o_need // o_bots + (1 if o_need % o_bots else 0)
            dtime = max(0, dtime)

            if dtime < time_left: 
                res.append(get_max_num_geodes(time_left - dtime - 1,
                                                ore      + (dtime + 1)*o_bots - o_to_c,
                                                clay     + (dtime + 1)*c_bots,
                                                obsidian + (dtime + 1)*obs_bots,
                                                geodes   + (dtime + 1)*g_bots,
                                                o_bots,
                                                c_bots   + 1,
                                                obs_bots,
                                                g_bots))
                                            
        # if it makes sense, try making one obsidian bot next
        if c_bots > 0 and obs_bots < obs_to_g:
            o_need = o_to_obs - ore
            c_need = c_to_obs - clay

            dtime1 = o_need // o_bots + (1 if o_need % o_bots else 0)
            dtime2 = c_need // c_bots + (1 if c_need % c_bots else 0)

            dtime = max(dtime1, dtime2, 0)

            if dtime < time_left: 
                res.append(get_max_num_geodes(time_left - dtime - 1,
                                                ore      + (dtime + 1)*o_bots - o_to_obs,
                                                clay     + (dtime + 1)*c_bots - c_to_obs,
                                                obsidian + (dtime + 1)*obs_bots,
                                                geodes   + (dtime + 1)*g_bots,
                                                o_bots,
                                                c_bots,
                                                obs_bots + 1,
                                                g_bots))


        # pick the scenario with the best outcome
        return max(res)

    return get_max_num_geodes(time_available, 0, 0, 0, 0, 1, 0, 0, 0)

#####
# Problem 1
#####

for blueprint in blueprints:

    # blueprint id, various costs of the robots
    digits = list(map(int, re.findall('\d+', blueprint)))
    blueprint_id = digits[0]
    costs = digits[1:]

    max_num_geodes = process_blueprint(costs, 24)

    quality_levels_sum += max_num_geodes * blueprint_id
    
print(quality_levels_sum)

#####
# Problem 2
#####

result = 1

for blueprint in blueprints[:3]:

    # blueprint id, various costs of the robots
    digits = list(map(int, re.findall('\d+', blueprint)))
    blueprint_id = digits[0]
    costs = digits[1:]

    result *= process_blueprint(costs, 32)

print(result)

