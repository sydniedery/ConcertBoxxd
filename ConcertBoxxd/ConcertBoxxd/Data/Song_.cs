namespace ConcertBoxxd.Data
{
    public class Song_
    {
        public int ID { get; set; }
        public string Name { get; set; }

        public Song_()
        { }
        public Song_(int id, string name)
        {
            ID = id;
            Name = name;
        }


        //might need to add a ToString() override
    }
}
