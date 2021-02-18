@echo off
rem copyright: 2020-2021, Frederico Martins
rem author: Frederico Martins <http://github.com/fscm>
rem license: SPDX-License-Identifier: MIT

rem Use python to execute the python script having the same name as this batch
rem file, but without any extension, located in the same directory as this
rem batch file
"%~dpn0" %*
