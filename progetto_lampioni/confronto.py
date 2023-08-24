from pprint import pprint
import numpy as np

def euclidean_distance(tuple1, tuple2):
    return np.sqrt(sum((x - y) ** 2 for x, y in zip(tuple1, tuple2)))

def find_similar_tuples(array1, array2, threshold):
    result = []
    for tuple1 in array1:
        for tuple2 in array2:
            distance = euclidean_distance(tuple1, tuple2)
            if distance <= threshold:
                result.append(1)
                array2.remove(tuple2)
                print("sono nell'if")
                print(tuple1)
                print(tuple2)
                break
            else:
                result.append(0)
                print("sono nell'else")
                print(tuple1)
                print(tuple2)
                continue
    remaining_tuples = abs(len(array2) - len(array1))
    result.extend([0] * remaining_tuples)

    return result



tuple1 = [(0.0, 0.2625, 0.47265625, 0.02421875, 0.0484375), (0.0, 0.3015625, 0.60625, 0.01640625, 0.0359375), (0.0, 0.48671875, 0.50703125, 0.0203125, 0.03984375), (0.0, 0.44296875, 0.58671875, 0.015625, 0.0234375)]
tuple2 = [(0.0, 0.2625, 0.47265625, 0.02421875, 0.0484375),
 (0.0, 0.28515625, 0.5609375, 0.015625, 0.03125),
 (0.0, 0.3015625, 0.60625, 0.01640625, 0.0359375),
 (0.0, 0.6640625, 0.3015625, 0.0296875, 0.04375),
 (0.0, 0.48671875, 0.50703125, 0.0203125, 0.03984375),
 (0.0, 0.44296875, 0.58671875, 0.015625, 0.0234375),
 (0.0, 0.50546875, 0.5328125, 0.01328125, 0.01953125),
 (0.0, 0.43203125, 0.56875, 0.0125, 0.025),
 (0.0, 0.49609375, 0.53671875, 0.0109375, 0.0203125),
 (0.0, 0.40234375, 0.60625, 0.015625, 0.028125),
 (0.0, 0.34453125, 0.6515625, 0.01015625, 0.021875),
 (0.0, 0.3859375, 0.6234375, 0.0109375, 0.025),
 (0.0, 0.27109375, 0.6625, 0.01484375, 0.03515625),
 (0.0, 0.3, 0.67734375, 0.015625, 0.0265625)]

res = find_similar_tuples(tuple1, tuple2, 0.0001)



print(res)
print(tuple1)
print(tuple2)

