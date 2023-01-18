import re
scan = open('16.txt', 'r').read().splitlines()

# collect a list of rates and a dictionary describing the graph (vertex: neighbors)
vertices = []
rates = {}
graph = {}

for row in scan:
    rate = int(re.findall('\d+', row)[0])
    v = re.findall('[A-Z][A-Z]', row)

    vertices.append(v[0])
    graph[v[0]] = v[1:]
    rates[v[0]] = rate

# build a distance matrix using Dijkstra

def distances_from_vertex(start):
    """
    Return distances of all vertices from vertex "start" (as a dictionary vertex:distance)
    """

    distances = {v: 10**9 for v in vertices}
    fixed = {v: False for v in vertices}

    distances[start] = 0

    for _ in vertices:

        # find the vertex with smallest distance
        smallest_distance = 10**9
        vertex_to_fix = None

        for i, di in distances.items():
            if not fixed[i] and di < smallest_distance:
                smallest_distance = di
                vertex_to_fix = i

        # make it permanent
        fixed[vertex_to_fix] = True

        # update distances to other vertices
        for neighbor in graph[vertex_to_fix]:
            if not fixed[neighbor]:
                distances[neighbor] = min(distances[neighbor], smallest_distance + 1)

    return distances
                
distances = {v: distances_from_vertex(v) for v in vertices}

# we only need to care about AA and the vertices with nonzero rates
important = ['AA'] + [v for v, rate in rates.items() if rate > 0]

# how long it takes to travel between important vertices and also open a valve at the
# final vertex (+1 for this)
distances = {v: {v2: d+1 for v2, d in distances[v].items() if v2 in important} 
            for v in vertices if v in important}

#####
# Problem 1
#####

def get_max_pressure(time_left, position, visited, total_rate, total_pressure):

    possibilities = []

    # check which of the "important" vertices we should visit next
    for v in important:
        if v not in visited and distances[position][v] < time_left:
            dt = distances[position][v]
            possibilities.append(get_max_pressure(time_left - dt,
                                                    v,
                                                    visited + [v],
                                                    total_rate + rates[v],
                                                    total_pressure + dt * total_rate)
                                )

    if len(possibilities) == 0:
        # we can not get to any other vertex in time
        return total_pressure + total_rate * time_left
    else:
        # pick the optimal solution
        return max(possibilities)

print(get_max_pressure(30, 'AA', [], 0, 0))

#####
# Problem 2
#####

def get_max_pressure2(time_left, direction1, time_left_move1, direction2, time_left_move2, 
            vertices_left, total_rate, total_pressure):
    """
    How much pressure can we release? direction1 = where I am headed, direction2 = where
    elephant is headed, vertices_left = list of vertices we have not yet visited (and are
    not yet scheduled to visit at a later time). Time_left_moveX are times until we reach
    the vertex we are headed to.  At least one of them should be zero, indicating we have
    just arrived at a vertex (and finished turning the valve on). Total_rate is the sum of
    rates of the valves that are already open (before turning valves at directionX).
    """

    assert time_left_move1 == 0 or time_left_move2 == 0

    # Update rates by adding the newly visited vertices
    new_rate = total_rate
    if time_left_move1 == 0:
        new_rate += rates[direction1]
    if time_left_move2 == 0:
        new_rate += rates[direction2]

    # try assigning new vertex to whoever needs one. Optimize over all
    # possibilities.
    possibilities = []

    # I need more time to finish the move, elephant needs a new goal
    if time_left_move1 > 0 and time_left_move2 == 0:
        # One possibility is that elephant is done. Send him to AA in the time left.
        dt = time_left_move1
        possibilities.append(get_max_pressure2(time_left - dt,
                                                direction1,
                                                time_left_move1 - dt,
                                                'AA',
                                                time_left - dt,
                                                vertices_left,
                                                new_rate,
                                                total_pressure + dt * new_rate)
                            )

        # Otherwise try to pick a valve to open
        for v2 in vertices_left:
            if  distances[direction2][v2] < time_left:
                dt2 = distances[direction2][v2]
                dt = min(dt2, time_left_move1)
                possibilities.append(get_max_pressure2(time_left - dt,
                                                        direction1,
                                                        time_left_move1 - dt,
                                                        v2,
                                                        dt2 - dt,
                                                        vertices_left - set([v2]),
                                                        new_rate,
                                                        total_pressure + dt * new_rate)
                                    )

    # Elephant needs more time to move, I need a goal
    if time_left_move2 > 0 and time_left_move1 == 0:
        # One possibility is that we are done. Send use to AA in the time left.
        dt = time_left_move2
        possibilities.append(get_max_pressure2(time_left - dt,
                                                'AA',
                                                time_left - dt,
                                                direction2,
                                                time_left_move2 - dt,
                                                vertices_left,
                                                new_rate,
                                                total_pressure + dt * new_rate)
                            )

        # Otherwise assign us one of the remaining vertices
        for v1 in vertices_left:
            if  distances[direction1][v1] < time_left:
                dt1 = distances[direction1][v1]
                dt = min(dt1, time_left_move2)
                possibilities.append(get_max_pressure2(time_left - dt,
                                                        v1,
                                                        dt1 - dt,
                                                        direction2,
                                                        time_left_move2 - dt,
                                                        vertices_left - set([v1]),
                                                        new_rate,
                                                        total_pressure + dt * new_rate)
                                    )

    # We both need a new vertex
    if time_left_move1 == 0 and time_left_move2 == 0:
        if len(vertices_left) == 0:
            pass
        if len(vertices_left) == 1:
            # only one of us has to go to a new destination. Try both possibilities and
            # send the other to 'AA'.
            for v1 in vertices_left:
                if distances[direction1][v1] < time_left:
                        dt = distances[direction1][v1]
                        possibilities.append(get_max_pressure2(time_left - dt,
                                                                v1,
                                                                0,
                                                                'AA',
                                                                time_left - dt,
                                                                vertices_left - set([v1]),
                                                                new_rate, 
                                                                total_pressure + dt * new_rate)
                                            )

            for v2 in vertices_left:
                if distances[direction2][v2] < time_left:
                        dt = distances[direction2][v2]
                        possibilities.append(get_max_pressure2(time_left - dt,
                                                                'AA',
                                                                time_left - dt,
                                                                v2,
                                                                0,
                                                                vertices_left - set([v2]),
                                                                new_rate, 
                                                                total_pressure + dt * new_rate)
                                            )
        else:
            # we both can find a new goal
            for v1 in vertices_left:
                if distances[direction1][v1] < time_left:
                    for v2 in vertices_left:
                        if (v1 != v2) and (distances[direction2][v2] < time_left):
                            dt1 = distances[direction1][v1]
                            dt2 = distances[direction2][v2]
                            dt = min(dt1, dt2)
                            possibilities.append(get_max_pressure2(time_left - dt,
                                                                    v1,
                                                                    dt1 - dt,
                                                                    v2,
                                                                    dt2 - dt,
                                                                    vertices_left - set([v1, v2]),
                                                                    new_rate, 
                                                                    total_pressure + dt * new_rate)
                                                )
                    
    if len(possibilities) == 0:
        # we can not get to any other vertex in time, finish by inertia
        return total_pressure + new_rate * time_left
    else:
        # pick the optimal solution from the possibilities we found
        return max(possibilities)

print(get_max_pressure2(26, 'AA', 0, 'AA', 0, set(important[1:]), 0, 0))
