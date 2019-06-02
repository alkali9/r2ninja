# plugin to do r2 stuff 
import os

# this is the default r2 inst dir on macOS
# not included in the binja script PATHs
os.environ["PATH"] += ":/usr/local/bin"

from binaryninja import *
import r2pipe

class R2Ninja:

	def __init__(self):
		self.initialized = False

	def log(self, message, level=1):
		log.log(level, message)

	def initialize(self, bv):
		self.log("Starting r2ninja")
		self.r2p = r2pipe.open(bv.file.filename, flags=["-N"])
		self.path = bv.file.filename
		self.binary = bv.file.filename.split("/")[-1]
		self.zig_name = "%s.zig" % self.path

		self.r2p.cmd("aaa")

		self.initialized = True

	def disassemble(self, bv, function):
		disass = self.r2p.cmd("pdf @ %d" % function.start)
		self.log(disass)

	def decompile(self, bv, function):
		dec = self.r2p.cmd("pdd @ %d" % function.start)
		self.log(dec)

	def isInitialized(self, bv=None, addr=None):
		return self.initialized

	def execCommand(self, bv):
		text = get_text_line_input("Enter command: ", "getCommand")

		if text != None:
			self.log(self.r2p.cmd(text))

	def seek(self, bv, address):
		self.r2p.cmd("s %d" % address)
		self.log("r2 is at [%016x]" % address)

	# TODO: synce all the symbols and do it better
	def sync(self, bv):

		self.log("Syncing symbols...")

		# read the symbols from r2 and apply to bn
		imports = self.r2p.cmdj("fs imports; fj")
		symbols = self.r2p.cmdj("fs functions; fj")

		#sometimes binja does a bad job getting imports
		for imp in imports:
			name = imp["name"].split(".")[-1]
			bn_imp = bv.get_symbol_at(imp["offset"])
			if bn_imp == None:
				self.log("Adding import: %s" % name)
				bv.add_function(imp["offset"])
				s = Symbol(SymbolType.ImportedFunctionSymbol, imp["offset"], name)
				bv.define_user_symbol(s)
			elif name != bn_imp.name:
				self.log("Import %s already defined as %s" % (name, bn_imp.name))

		for sym in symbols:
			name = sym["name"]
			bn_sym = bv.get_symbol_at(sym["offset"])
			if bn_sym == None:
				self.log("Adding function: %s" % name)
				bv.add_function(imp["offset"])
				s = Symbol(SymbolType.FunctionSymbol, sym["offset"], name)
				bv.define_user_symbol(s)
			elif name != bn_sym.name:
				self.log("Symbol %s already defined as %s" % (name, bn_sym.name))

		# read the symbols from bn and apply to r2
		bn_symbols = bv.get_symbols()

		for sym in bn_symbols:
			if sym.type == SymbolType.FunctionSymbol:

				try:
					r2_sym = self.r2p.cmdj("fs functions; fdj %d" % sym.address)
				except:
					r2_sym = None

				if r2_sym == None:
					self.r2p.cmd("f %s @ %d" % (sym.name, sym.address))
					self.log("Defined '%s' in r2" % sym.name)

				elif r2_sym["name"][:3] == "fcn" and sym.name != r2_sym["name"]:
					self.r2p.cmd("fr %s %s" % (r2_sym["name"], sym.name))
					self.log("Renamed '%s' in r2" % sym.name)

	def saveProject(self, bv):
		project_name = "%s-r2bn" % self.binary
		self.r2p.cmd("Ps %s" % project_name)
		self.log("Saved project '%s'" % project_name)

	def loadProject(self, bv):
		project_name = get_text_line_input("Enter project: ", "getProject")

		if project_name == None:
			return

		elif project_name == "":
			project_name = "%s-r2bn" % bv.file.filename

		self.r2p.cmd("Po %s" % project_name)
		self.log("Opened project '%s'" % project_name)

	def saveZig(self, bv):
		zout = self.r2p.cmd("zg")
		self.log(zout)
		self.r2p.cmd("zos %s" % self.zig_name)
		self.log("Saved zignatures '%s'" % self.zig_name)

	def loadZig(self, bv):
		zig_name = get_open_filename_input("Enter zig file: ", "")

		if zig_name == None:
			return

		elif zig_name == "":
			zig_name = self.zig_name

		self.r2p.cmd("zo %s" % zig_name)
		self.log("Opened zignatures '%s'" % zig_name)

	def interactive(self):
		cmd = ""
		while cmd != "q":
			loc = self.r2p.cmdj("pdj 1")[0]["offset"]
			cmd = raw_input("[%016x]> " % loc)

			if cmd != "q" and cmd != "":
				print(self.r2p.cmd(cmd))

r2ninja = R2Ninja()

def interactive():
	r2ninja.interactive()

PluginCommand.register("Execute r2 command", "Executes r2 command", r2ninja.execCommand, r2ninja.isInitialized)
PluginCommand.register("Save r2 project", "Saves an r2 project", r2ninja.saveProject, r2ninja.isInitialized)
PluginCommand.register("Load r2 project", "Loads an r2 project", r2ninja.loadProject, r2ninja.isInitialized)
PluginCommand.register("Save r2 zignatures", "Saves an r2 zig file", r2ninja.saveZig, r2ninja.isInitialized)
PluginCommand.register("Load r2 zignatures", "Loads an r2 zig file", r2ninja.loadZig, r2ninja.isInitialized)
PluginCommand.register_for_address("Seek r2 to address ", "Sets the current address in r2", r2ninja.seek, r2ninja.isInitialized)
PluginCommand.register_for_function("Decompile with r2dec", "Decompiles function with r2dec", r2ninja.decompile, r2ninja.isInitialized)
PluginCommand.register_for_function("Disassemble with r2", "Disassembles function with r2", r2ninja.disassemble, r2ninja.isInitialized)
PluginCommand.register("Sync symbols", "Sync symbols with r2", r2ninja.sync, r2ninja.isInitialized)
PluginCommand.register("Initialize r2ninja", "Start r2ninja", r2ninja.initialize)