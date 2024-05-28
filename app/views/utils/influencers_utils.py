class Influencer_details:
    def to_numeric(self, str_num):
        if str_num[-1] == 'm':
            numeric = int(float(str_num[:-1]) * 1e6)

        elif str_num[-1] == 'b':
            numeric = int(float(str_num[:-1]) * 1e9)

        elif str_num[-1] == 'k':
            numeric = int(float(str_num[:-1]) * 1000)

        else:
            numeric = int(str_num)
        return numeric
