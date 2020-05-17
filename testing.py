from fractions import Fraction  
def answer(pegs):
    arr_length = len(pegs)
    if ((not pegs) or arr_length == 1):
        return [-1,-1]

    even = True if (arr_length % 2 == 0) else False
    sum = (- pegs[0] + pegs[arr_length - 1]) if even else (- pegs[0] - pegs[arr_length -1])

    if (arr_length > 2):
        for index in xrange(1, arr_length-1):
            sum += 2 * (-1)**(index+1) * pegs[index]

    first_gear_radius = Fraction(2 * (float(sum)/3 if even else sum)).limit_denominator()

    # now that we have the radius of the first gear, we should again check the input array of pegs to verify that
    # the pegs radius' is atleast 1.
    # since for valid results, LastGearRadius >= 1 and first_gear_radius = 2 * LastGearRadius
    # thus for valid results first_gear_radius >= 2

    if first_gear_radius < 2:
        return [-1,-1]

    current_radius = first_gear_radius
    for index in xrange(0, arr_length-2):
        center_distance = pegs[index+1] - pegs[index]
        next_radius = center_distance - current_radius
        if (current_radius < 1 or next_radius < 1):
            return [-1,-1]
        else:
            current_radius = next_radius

    return [first_gear_radius.numerator, first_gear_radius.denominator]