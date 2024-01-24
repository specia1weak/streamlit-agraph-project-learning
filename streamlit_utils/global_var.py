class VarInStreamlit(object):
    def __init__(self, streamlit_page, name, init_obj=None, init_fn=None):
        self.st = streamlit_page
        self.name = name
        if name not in self.st.session_state:
            self.st.session_state[name] = init_obj
            if init_fn:
                init_fn(self.st.session_state[name])

    def get(self):
        return self.st.session_state[self.name]

    def set(self, x):
        self.st.session_state[self.name] = x

    def delete(self):
        del self.st.session_state[self.name]

    val = property(get, set, delete)

