def increasing_boi():
    n = input()
    nums = input()
    nums = [int(num) for num in nums.split(" ")]

    count = 0
    for i in range(1, len(nums)):
        if nums[i] < nums[i - 1]:
            count += -(nums[i] - nums[i - 1])
            nums[i] = nums[i - 1]

    return count


print(increasing_boi())