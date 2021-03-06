from unicon.statemachine import State, Path, StateMachine
from .statements import KpStatements
from .patterns import KpPatterns
from .dialogs import KpDialogs


class KpStateMachine(StateMachine):
    """An SSP class that restores all states."""
    def __init__(self, patterns):
        """Initializer of SspStateMachine."""

        self.patterns = patterns
        self.dialogs = KpDialogs(patterns)
        self.statements = KpStatements(patterns)
        super().__init__()

    def create(self):
        # Create States and their state patterns
        prelogin_state = State('prelogin_state', self.patterns.prompt.prelogin_prompt)
        fxos_state = State('fxos_state', self.patterns.prompt.fxos_prompt)
        fireos_state = State('fireos_state', self.patterns.prompt.fireos_prompt)
        expert_state = State('expert_state', self.patterns.prompt.expert_prompt)
        sudo_state = State('sudo_state', self.patterns.prompt.sudo_prompt)
        rommon_state = State('rommon_state', self.patterns.prompt.rommon_prompt)
        local_mgmt_state = State('local_mgmt_state', self.patterns.prompt.local_mgmt_prompt)

        # lina cli states
        enable_state = State('enable_state', self.patterns.prompt.enable_prompt)
        disable_state = State('disable_state', self.patterns.prompt.disable_prompt)
        config_state = State('config_state', self.patterns.prompt.config_prompt)

        # Add our states to the state machine
        self.add_state(prelogin_state)
        self.add_state(fxos_state)
        self.add_state(fireos_state)
        self.add_state(expert_state)
        self.add_state(sudo_state)
        self.add_state(rommon_state)
        self.add_state(local_mgmt_state)
        self.add_state(enable_state)
        self.add_state(disable_state)
        self.add_state(config_state)

        # Create paths for switching between states
        prelogin_to_fxos = Path(prelogin_state, fxos_state, '', self.dialogs.d_prelogin_to_fxos)
        fxos_to_prelogin = Path(fxos_state, prelogin_state, 'top; exit', None)
        fxos_to_ftd = Path(fxos_state, fireos_state, "connect ftd", None)
        fxos_to_local_mgmt = Path(fxos_state, local_mgmt_state, "connect local-mgmt", None)
        ftd_to_expert = Path(fireos_state, expert_state, "expert", None)
        ftd_expert_to_sudo = Path(expert_state, sudo_state, "sudo su -", self.dialogs.d_expert_to_sudo)
        ftd_sudo_to_expert = Path(sudo_state, expert_state, "exit", None)
        expert_to_ftd = Path(expert_state, fireos_state, "exit", None)
        local_mgmt_to_fxos = Path(local_mgmt_state, fxos_state, "exit", None)
        ftd_to_fxos = Path(fireos_state, fxos_state, "connect fxos", self.dialogs.d_ftd_to_fxos)

        # Crete lina cli paths
        expert_to_disable_path = Path(expert_state, disable_state, 'sudo lina_cli',
                                      self.dialogs.ftd_dialogs.d_expert_to_disable)
        fireos_to_disable_state = Path(fireos_state, disable_state,
                                       'system support diagnostic-cli',
                                       self.dialogs.ftd_dialogs.d_enable_to_disable)
        fireos_to_enable_state = Path(fireos_state, enable_state,
                                      'system support diagnostic-cli',
                                      self.dialogs.ftd_dialogs.d_disable_to_enable)
        fireos_to_config_state = Path(fireos_state, config_state,
                                      'system support diagnostic-cli',
                                      self.dialogs.ftd_dialogs.d_endisable_to_conft)
        disable_to_enable_state = Path(disable_state, enable_state, 'en',
                                       self.dialogs.ftd_dialogs.disable_to_enable)
        enable_to_disable_state = Path(enable_state, disable_state, "disable", None)

        disable_to_fireos_path = Path(disable_state, fireos_state, '\001'+'d'+'exit',
                                      None)

        enable_to_config_path = Path(enable_state, config_state, 'conf t', None)
        config_to_enable_path = Path(config_state, enable_state, 'end', None)

        # Add paths to the State Machine
        self.add_path(prelogin_to_fxos)
        self.add_path(fxos_to_prelogin)
        self.add_path(fxos_to_ftd)
        self.add_path(fxos_to_local_mgmt)
        self.add_path(ftd_to_expert)
        self.add_path(ftd_expert_to_sudo)
        self.add_path(ftd_sudo_to_expert)
        self.add_path(expert_to_ftd)
        self.add_path(ftd_to_fxos)
        self.add_path(local_mgmt_to_fxos)
        self.add_path(expert_to_disable_path)
        self.add_path(fireos_to_disable_state)
        self.add_path(fireos_to_enable_state)
        self.add_path(fireos_to_config_state)
        self.add_path(disable_to_enable_state)
        self.add_path(enable_to_disable_state)
        self.add_path(disable_to_fireos_path)
        self.add_path(enable_to_config_path)
        self.add_path(config_to_enable_path)

        # after inactivity timer, it will go back to prelogin:
        self.add_default_statements(self.statements.login_password)
