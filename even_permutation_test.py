import numpy as np

class PermutableNdArray(np.ndarray):
    """Use 'Even's Speedup' of the Steinhaus–Johnson–Trotter algorithm
    to modify the given buf with the given current 'speeds' to yield the
    next permutation of the buf.
    """
    def __init__(self, shape, dtype, buffer, offset, strides, order) -> None:
        super().__init__(shape, dtype=dtype, buffer=buffer, offset=offset, strides=strides, order=order)

        # Make array to hold speeds. Set first slot to 0 and all other slots to -1
        self.__speeds = np.full(self.size, -1)
        self.__speeds[0] = 0

        # Set active element index to last element
        self.__act_index = self.size - 1

        # TODO: Wait...I need to also keep have each element labeled with their original position in the list
        # ...this is a lot of info per spot...would really be nice to have an object at each position...
        # ...hm...maybe this class is just something that is able to permutate and keep track of permutation
        # state for some external array...hmm...

    def permutate(self):
        """Modify the buf to get the next permutation of the array
        """
        # Swap active element with element to its left when speed is -1
        if self.__speeds[self.__act_index] == -1:
            # Save left value and speed
            temp = self[self.__act_index - 1]
            temp_speed = self.__speeds[self.__act_index -1]

            # Perform swap of values using temp
            self[self.__act_index - 1] = self[self.__act_index]
            self[self.__act_index] = temp

            # Perform swap of speeds using temp
            self.__speeds[self.__act_index - 1] = self.__speeds[self.__act_index]
            self.__speeds[self.__act_index] = temp_speed

            # Decrement the active index
            self.__act_index -= 1
        # Swap active element with element to its right when speed is +1
        elif self.__speeds[self.__act_index] == 1:
            pass
        # If active element is 0, I think that means we're on the final permutation
        # ...so...just swap the first two elements?
        else:
            pass

        # Do step where all elements that are larger than the active one
        # are given a +/1 in the direction of the active element
        if "something":
            pass
        # If active index is now 0 or max, then set this speed to 0
        # and go through whole array to find largest element and set that
        # index to the active index
        elif self.__act_index == 0 or self.__act_index == (self.size -1):
            pass 


if __name__ == "__main__":
    perm_array = PermutableNdArray([0, 1, 2, 3], dtype=np.uint8)
    print(perm_array)
    perm_array.permutate()
    print(perm_array)
