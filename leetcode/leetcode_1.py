class Solution:
    def sum(self, l):
        sum = 0
        for i in l:
            sum += i
        return sum
    """
    1 给定一个整数数组 A，返回其中元素之和可被 K 整除的（连续、非空）子数组的数目。
    输入：A = [4,5,0,-2,-3,1], K = 5
    输出：7
    解释：
    有 7 个子数组满足其元素之和可被 K = 5 整除：
    [4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]
    链接：https://leetcode-cn.com/problems/subarray-sums-divisible-by-k
    """
    def subarraysDivByK_2(self, A, K):
        """
        双层for循环，暴力求解，遍历所有的连续子数组，时间复杂度O(n^2), 数组过大时，leetcode上超时，未能AC
        """
        a_len = len(A)
        if a_len == 1:
            return 1 if A[0] % K == 0 else 0
        count = 0
        for start in range(a_len-1):
            for end in range(start+1, a_len+1):
                temp = A[start:end]
                if self.sum(temp) % K == 0:
                    count += 1
        if A[-1] % K == 0:
            count += 1
        return count

    """
        前缀和：数组中前 i 项的和
        同余定理：如果两个数 mod k 得到相同的余数，那么这两数的差一定是 k 的倍数 a = mk + d; c = nk + d; a - c = (m - n)k
        连续子数组的和可以表示为前缀和的差 如：s[i:j] = s[j] - s[i-1]
        
        方法：1 求出所有的前缀和
             2 求出所有前缀和 mod K 的余数
             3 用hash表统计每个余数的个数
             4 余数大于等于2 就证明存在连续子数组的的组合，对于余数为0来说 本身就可以构成一个被K整除的数组
        时间复杂度 O(n), 空间复杂度 O(n)
    """
    def subarraysDivByK(self, A, K):
        a_len = len(A)
        d = {}
        mod = 0
        s = 0
        for i in range(a_len):
            # 求前缀和的余数 这种方法更简单：mod(s[j]) = mod(mod(s[j-1]) + A[j]) 当然也可以这样：
            s += A[i]
            mod = s % K
            # mod = (mod + A[i]) % K
            if d.get(mod) is None:
                d[mod] = 1
            else:
                d[mod] += 1
        count = 0
        print(d)
        for key, value in d.items():
            if key == 0:
                count += (value + value * (value - 1) / 2)
            else:
                count += (value * (value - 1)) / 2
        return int(count)

    # 网上另外一种python实现方法
    def subarraysDivByK_3(self, A, K):
        # 余数为0的话 本身就可以构成一个数组 赋值为1
        record = {0: 1}
        total, ans = 0, 0
        for elem in A:
            total += elem
            modulus = total % K
            # 不为0的余数 赋值0，因为相同余数必须要大于1 才能构成符合要求的连续子数组
            same = record.get(modulus, 0)
            # 其实是一个排列组合 但这里用到了一个等式代替
            # Cn2 = n(n-1)/2 = 1 + 2 + 3 + ....... + n-1 = (n-1 + 1)*(n-1)/2
            ans += same
            record[modulus] = same + 1
        print(record)
        return ans


if __name__ == '__main__':
    s = Solution()
    print(s.subarraysDivByK_2([8,9,7,8,9], 8))
    print(s.subarraysDivByK([8,9,7,8,9], 8))
    print(s.subarraysDivByK_3([8,9,7,8,9], 8))