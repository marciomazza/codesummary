from codesummary import summarize


def load_ipython_extension(ipython):

    from prompt_toolkit.document import Document

    if not hasattr(ipython, "pt_app"):
        print(
            "This plugin works only with prompt toolkit."
            " No instance os prompt toolkit found."
        )

    @ipython.pt_app.key_bindings.add_binding("f3")
    def summarize_history(event):
        buffer = ipython.pt_app.default_buffer
        history = [
            stmt
            for _, _, stmt in ipython.history_manager.get_range(raw=False)
            # filter out IPython magics
            if not stmt.startswith("get_ipython().run_")
        ]
        summary = summarize(history)
        buffer.document = Document("\n".join(summary))
