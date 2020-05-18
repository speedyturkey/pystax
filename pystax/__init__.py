"""
Stax.load_staxfile
begin
  Stax::Cli.start(ARGV)
rescue Aws::CloudFormation::Errors::ExpiredToken => e
  abort(e.message)
end

"""
from pystax import stax

stax.load_staxfile()
