from Cylinder import Cylinder
import random, base64, math


class Enigma():
    def __init__(self, password, cylinders=3, text_encoding="utf-32-le", steckerbrett={}):
        '''
            Used to setup the Enigma machine.
            Note: Text encoding is utf-32-le to support
            almost every possible char, but it uses
            a lot of bits for char encoding, so if you
            are not using strange chars, please use
            utf-8/utf-16.

            Also, the number of cylinders
            have to be at least 3, and might be more based on
            the password lenght. With this config, we have at least
            65^3 possible combinations.

            :param password:
            :param cylinders:
            :param text_encoding:
        '''

        self.text_encoding = text_encoding
        self.cylinders = []
        self.reflectors = []
        self.min_password_length = 12
        self.min_cylinders = 3
        self.desired_cylinders = int(cylinders)
        self.seeds = self.generate_seeds(password)
        self.steckerbrett = steckerbrett
        self.init_steckerbrett()
        self.init_cylinders()

    def return_reflector(self, seed, reverse=False):
        '''
            This returns the reflector, that is a basic shuffled
            dictionary that associates a letter to another
            letter in a bijective way.

            NOTE: We are using Cylinder.base_alphabeth(),
            that is a @staticfunction.

            :param seed:
            :param reverse:
            :return: dictionary
        '''

        random.seed(seed)
        data = {}
        base_alphabeth = Cylinder.base_alphabeth()
        reflector = Cylinder.base_alphabeth()
        random.shuffle(reflector)
        for i in range(len(Cylinder.base_alphabeth())):
            if not reverse:
                data[base_alphabeth[i]] = reflector[i]
            else:
                data[reflector[i]] = base_alphabeth[i]
        return data

    def generate_seeds(self, password):
        '''
            This function divides the password in
            a predefined number of lists, the number of list
            is equal to the number of cylinders.

            After this, it transforms every letter of the list to
            the ascii value of the letter, and it multiplies this value.
            EX: "abc" is ascii_of(a)*ascii_of(b)*ascii_of(c)
            and this returned value will become the seed of the cylinder

            :param password:
            :return:
        '''

        seeds = []
        divided_password = []
        password_size_for_seed = math.ceil(len(password) / int(self.desired_cylinders))
        if len(password) < self.min_password_length:
            raise ValueError("Insufficient password length.")
        if self.desired_cylinders < self.min_cylinders:
            raise ValueError("Insufficient cylinders number.")
        for i in range(0, len(password), password_size_for_seed):
            divided_password.append(password[i:i + password_size_for_seed])
        for division in divided_password:
            seed = 1.1
            for letter in division:
                # seed *= ord(letter)
                seed *= math.log(ord(letter), 2)
            seed = 10**(math.log(seed, 2))
            seeds.append(seed)
        return seeds

    def molt_of_seeds(self):
        '''
            This fuction returns the moltiplication of the seeds used.

            :return:
        '''

        sum_of_seeds = 0
        for seed in self.seeds:
            sum_of_seeds *= seed
        return sum_of_seeds

    def init_cylinders(self):
        '''
            Reset cylinder status, used for cypher
            or decypher a text.

            :return:
        '''

        self.cylinders = [Cylinder(seed=seed) for seed in self.seeds]
        self.reflectors = [self.return_reflector(seed=self.molt_of_seeds()),
                           self.return_reflector(reverse=True, seed=self.molt_of_seeds())]

    def crypt_steckerbrett(self, temp_letter):
        letter_in_steckerbrett = self.steckerbrett.get(temp_letter, False)
        if letter_in_steckerbrett:
            # if a value is false then will be skipped.
            return letter_in_steckerbrett
        return temp_letter

    def decypher_text(self, text):
        return self.cypher_text(text, decypher=True)

    def cypher_text(self, text, decypher=False):
        '''
            This function is used to cypher/decypher a text.

            :param text:
            :param decypher:
            :return:
        '''

        # reset the cylinders status.
        self.init_cylinders()
        if not decypher:
            # if we need to cypher the text, we need to encode it in base64
            text = base64.b64encode(bytes(text, self.text_encoding)).decode()
        # get the reflector for cyphering or decyphering a text/file.
        reflector = self.reflectors[int(decypher)]
        # initialize the cyphered text.
        cyphered_text = ""

        # cypher every letter in the text.
        for temp_letter in text:
            # first, let's pass this into the steckerbrett,
            # then, if it is present, we substitute the original value
            # with the one into the steckerbrett, and then
            # we pass this new value into the cylinders
            if not decypher:
                temp_letter = self.crypt_steckerbrett(temp_letter)

            # using the method for cyphering a letter,
            # cypher every letter in the text passing the output
            # of one cylinder to another.
            for cylinder in self.cylinders:
                temp_letter = cylinder.cypher(temp_letter)
            # pass the output to the reflector. We don't want
            # to decypher a cyphered text.
            temp_letter = reflector[temp_letter[0]]
            # reverse the order of the cylinders to
            # cypher the text once again.
            self.cylinders.reverse()
            # remake the procedure of cyphring the text
            # passing from the last cylinder to the first,
            # using reverse permutation.
            for cylinder in self.cylinders:
                temp_letter = cylinder.cypher(temp_letter, reverse_permutation=True)
            # after we cyphered the letter, we need to
            # rotate one or more cylinders.
            self.add_offset()
            # append the letter to the cyphered text variable.
            for cyphered_letter in temp_letter:
                cyphered_text += cyphered_letter
            # restore the cylinders list to the previous version.
            self.cylinders.reverse()

        # return the cyphered/decyphered text.
        if not decypher:
            return cyphered_text
        else:
            decyphered_text = ""
            for letter in cyphered_text:
                decyphered_text += self.crypt_steckerbrett(letter)
            # if it is decyphered, we now need to decode it from base64.
            bytes_data = bytes(decyphered_text, self.text_encoding)
            bytes_data = base64.b64decode(bytes_data)
            return bytes_data.decode(self.text_encoding)

    def add_offset(self):
        '''
            This function rotates the cylinders
            In particular: If the first rotor shifts,
            the also the second shifts. If the second
            rotor shifts, then the third shifts.
            If the second rotor doesn't shift, then
            also the third rotor stays still.
            :return:
        '''
        shift = True
        for cylinder in self.cylinders:
            if shift:   # Checks if the other rotor has to shift
                shift = cylinder.add_offset()
            else:
                break


    def cypher_file(self, path, decypher=False):
        '''
            This function load the file content, it
            cyphers/decyphers the text and then rewrites it.

            :param path:
            :param decypher:
            :return:
        '''

        with open(path, "r") as f:
            read_data = f.read()
            data = self.cypher_text(read_data,
                    decypher=decypher)
        with open(path, "w") as f:
            f.write(data)

    def init_steckerbrett(self, proportion=4, min_len=0):
        # the seed of steckerbrett is the
        # moltiplication between all the seeds
        seed = self.molt_of_seeds()
        random.seed(seed)
        alphabeth = Cylinder.base_alphabeth()
        if not self.steckerbrett:
            for letter in range(random.randint(min_len, len(alphabeth)//proportion)):
                key = random.sample(alphabeth, 1)[0]
                value = random.sample(alphabeth, 1)[0]

                alphabeth.remove(key)
                alphabeth.remove(value)
                self.steckerbrett[key] = value
                self.steckerbrett[value] = key