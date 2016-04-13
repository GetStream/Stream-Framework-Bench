package io.getstream.cassandra.locator;

import org.apache.cassandra.locator.SeedProvider;

import java.io.*;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.*;

public class FileSeedProvider implements SeedProvider {

    private static final String SEEDS_LIST_FILE = "/etc/cassandra/seeds.list";

    private List<InetAddress> addresses = new ArrayList<>();

    public FileSeedProvider(Map<String, String> args) {
        try {
            getIpsFromFile();
        } catch (FileNotFoundException e) {
            throw new RuntimeException("[ERROR][FileSeedProvider] Cannot read " + SEEDS_LIST_FILE);
        }
    }

    private void getIpsFromFile() throws FileNotFoundException {
        File seedFile = new File(SEEDS_LIST_FILE);

        Scanner scanner = new Scanner(new FileInputStream(seedFile));
        if (scanner.hasNextLine()) {
            try {
                addresses.add(getIpAddress(scanner.nextLine()));
                while (scanner.hasNextLine()) {
                    addresses.add(getIpAddress(scanner.nextLine()));
                }
            } catch (UnknownHostException e) {
                throw new RuntimeException("[ERROR][FileSeedProvider] Cannot parse ip address from " + SEEDS_LIST_FILE, e);
            }
        }
    }

    private InetAddress getIpAddress(String ipAsString) throws UnknownHostException {
        return InetAddress.getByName(ipAsString);
    }

    @Override
    public List<InetAddress> getSeeds() {
        return Collections.unmodifiableList(this.addresses);
    }

    public static void main(String[] args) {
        System.out.println(new FileSeedProvider(null).getSeeds());
    }
}
