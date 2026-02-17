import re

class RecoveryAgent:
    def apply_fix(self, original_command, diagnosis_report):
        potential_fixes = ["--low-mem", "--mem_mb", "--nprocs"]
        applied_fixes = [fix for fix in potential_fixes if fix in diagnosis_report]
        
        if not applied_fixes:
            return original_command

        # Clean the command: remove trailing backticks or whitespace
        clean_cmd = original_command.strip().replace("```bash", "").replace("```", "").strip()
        
        for fix in applied_fixes:
            if fix not in clean_cmd:
                clean_cmd += f" {fix}"
        
        # Wrap it back in a clean block
        return f"```bash\n{clean_cmd}\n```"