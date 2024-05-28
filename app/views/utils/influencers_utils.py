class InfluencerDetails:
    """
            Convert a string representation of a number with suffixes ('k', 'm', 'b') into an integer.

            :param str_num: A string representing a number potentially suffixed with 'k' for thousand,
                            'm' for million, or 'b' for billion. Examples: '1.5k', '2m', '3b', '100'.
            :return: The numeric value as an integer.
            """
    def to_numeric(self, str_num):
        if str_num[-1] == 'm':
            # Convert from millions to an integer
            numeric = int(float(str_num[:-1]) * 1e6)
        elif str_num[-1] == 'b':
            # Convert from billions to an integer
            numeric = int(float(str_num[:-1]) * 1e9)
        elif str_num[-1] == 'k':
            # Convert from thousands to an integer
            numeric = int(float(str_num[:-1]) * 1000)
        else:
            # Convert a plain numeric string to an integer
            numeric = int(str_num)
        return numeric
