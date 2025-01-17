
# Standard imports
import errno
import os
import subprocess
import tempfile


def form_value_using_dict(config, value, get_values_collection):
    ''' TODO Better name?
    '''
    assert isinstance(config, dict) and 0 < len(config)

    if config[value].isdigit():
        return {'id' : config[value]}

    else:
        values = [v.name for v in get_values_collection()]

        if config[value] in values:
            return {'name' : config[value]}

        raise RuntimeError('Given {} not in a list of allowed values: {}'.format(value, ', '.join(values)))


def interactive_edit(content):
    fd, filename = tempfile.mkstemp()                       # Make a temp file with current content
    os.write(fd, content.encode('utf8'))                    # Write initial content (if any) to it

    if 'EDITOR' not in os.environ:                          # Check if any editor has configured
        raise RuntimeError('`EDITOR` environment variable is not set. Don\'t know how to edit description...')

    rc = subprocess.run([os.environ['EDITOR'], filename])   # Start the editor and wait for end of editing

    # Get updated description
    st = os.fstat(fd)                                       # Get stats by file descriptor (iterested in updated size)
    os.lseek(fd, 0, os.SEEK_SET)                            # Rewind to the begining
    data = os.read(fd, st.st_size)                          # Read shole file

    os.unlink(filename)                                     # Clean temp file

    return data.decode('utf8')                              # Return updated content
