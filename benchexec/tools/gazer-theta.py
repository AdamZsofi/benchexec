# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.result as result
import benchexec.tools.template


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for gazer-theta
    (combined tool of Gazer and Theta)
    https://github.com/ftsrg/gazer
    https://github.com/ftsrg/theta
    """

    REQUIRED_PATHS = [".."]

    def executable(self, tool_locator):
        return tool_locator.find_executable("Portfolio.pl", subdir="scripts/portfolio")

    def name(self):
        return "gazer-theta"

    def version(self, executable):
        return self._version_from_tool(executable)

    def cmdline(self, executable, options, task, rlimits):
        # All of the flags should be added through the benchmark definition
        # (see Gazer docs on Portfolio and Benchexec)
        return [executable] + options + ["-t"] + [task.single_input_file]

    def determine_result(self, run):
        status = result.RESULT_UNKNOWN
        for line in run.output:
            if "Final result of portfolio: Verification FAILED" in line:
                status = result.RESULT_FALSE_REACH
            elif "Final result of portfolio: Verification SUCCESSFUL" in line:
                status = result.RESULT_TRUE_PROP

        if (
            not run.was_timeout
            and status == result.RESULT_UNKNOWN
            and run.exit_code.value != 0
        ):
            status = result.RESULT_ERROR

        return status
