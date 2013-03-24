class FieldReprer(object):
    def __repr__(self):
        fields = [
            str(k) + '=' + repr(v)
            for k, v in self.__dict__.iteritems()
            if '_' not in k and not hasattr(v, '__call__')
        ]

        return self.__class__.__name__ + '(' + ', '.join(fields) + ')'
