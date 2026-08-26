

def two_sum(nums: list[int], target: int) -> list[int]:


    for index in range(len(nums)):
        next_index = index + 1
        for next_index in range(next_index, len(nums)):
            if nums[index] + nums[next_index] == target:
                return [index, next_index]


    return [-1,-1]