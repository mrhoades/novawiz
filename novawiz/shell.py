
def main():
    try:
      print 'foobar'

    except Exception, e:
        logger.debug(e, exc_info=1)
        print >> sys.stderr, "ERROR: %s" % str(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
