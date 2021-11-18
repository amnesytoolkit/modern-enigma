import random

class Cylinder():
    def __init__(self, seed, offset=None, rotate_frequently=False, shift_every=None, legacy=False):
        '''
            This function is used to initialize the rotor.

            :param seed: Seed to enc/decrypt
            :param offset: Optional, it's
                            used for additional
                            security
            :param shift_every: Optional, if not
                                given will be random
                                generated. Used for
                                making the rotor shift
                                every x positions.
            :param legacy: Use this in case you want
                            to use the standard enigma.
            :param rotate_frequently: Generate a short offset
                                To let the rotor rotate frequently.
        '''

        self.seed = seed
        self.offset = offset
        self.legacy = legacy
        self.rotate_frequently = rotate_frequently

        '''
            If we haven't set the number of chars after
            we want the cylinder to shift, this will be 
            randomly generated. 
            Note that if we want to use the legacy version
            of enigma we will shift everytime the entire
            alfabeth is used.
            
        '''

        if not shift_every:
            if not self.legacy:
                random.seed(self.seed)
                # if it generates 0, it does not rotate at the first try.
                self.shift_every = random.randint(1, len(self.base_alphabeth())
                if not self.rotate_frequently else len(self.base_alphabeth())//4)
            else:
                self.shift_every = len(self.base_alphabeth())
        else:
            self.shift_every = int(shift_every)
            self.check_user_input(self.shift_every)

        if not offset:
            random.seed(self.seed)
            self.offset = random.randint(0,
                len(self.base_alphabeth()))
            self.check_user_input(self.offset)
        self.offset = self.offset % self.shift_every

    def check_user_input(self, data):
        if int(data) > len(self.base_alphabeth()):
            raise ValueError("Unable to set cylinder. Data is > than base_alphabeth")

    @staticmethod
    def base_alphabeth():
        '''
            Return the list of possible values returned by the base64.
            = is reserved for padding.
        :return:
        '''
        return list("ABCDEFGHIJKLMNOPQRSTUVWXYZa" +\
                    "bcdefghijklmnopqrstuvwxyz0123456789+/=")

    def obfuscated_alphabeth(self):
        '''
            This function will return the cyphered alfabeth
            used to cypher a letter/word in a dictionary
            (that is, an hashmap, to give the best performance
            considering that the finding time of an element is
            O(1).) based on the current cylinder settings.

            :return: a dictionary with the normal alfabeth
                    paired with the cyphered alfabeth
        '''

        # reset the seed to ensure that random
        # will always give the same result in
        # a deterministic way.
        random.seed(self.seed)

        # get the base alfabeth
        alphabeth = self.base_alphabeth()
        # get the base alfabeth,
        # we will shuffle this later on
        rotor_alphabeth = self.base_alphabeth()
        random.shuffle(rotor_alphabeth)

        '''
            Those lines checks the current offset of the rotor.
            An int(1) is added every time the rotor encrypts
            a letter in a two-way form. (that is it encrypt the 
            letter one time and then, after this letter is encrypted
            with the reflector, it reencrypts the letter another time
            with the same offset but with reverse permutation)
        '''
        if self.offset:
            offset = self.offset % self.shift_every
            rotor_alphabeth = rotor_alphabeth[offset:] + rotor_alphabeth[:offset]

        data = {}
        for i in range(len(self.base_alphabeth())):
            data[alphabeth[i]] = rotor_alphabeth[i]
        return data

    def add_offset(self):
        '''
            This function returns True/False if the
            cylinder has completed an entire rotation.
            This is used to rotate the other cylinder.

            :return: bool
        '''
        self.offset += 1
        if not self.offset % self.shift_every:
            self.offset = 0
            return True
        return False

    def cypher(self, data, reverse_permutation=False):
        '''
            returns the cyphered letter/sentence.
            For compatibility purposes we included the
            possibility to encrypt an entire word with only
            one cylinder, but we discourage using it because
            this is effectively only a ceasar encryption.

            :param data:
            :param reverse_permutation:
            :return:
        '''
        cyphered_text = []
        alphabeth = self.obfuscated_alphabeth()
        for letter in data:
            if reverse_permutation:
                cyphered_text.append(list(alphabeth.keys())[list(alphabeth.values()).index(letter)])
            else:
                cyphered_text.append(alphabeth[letter])
        return cyphered_text

