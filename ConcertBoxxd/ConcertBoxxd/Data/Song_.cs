namespace ConcertBoxxd.Data
{
    public class Song_
    {
        public int Id { get; set; }
        public string Name { get; set; }

        public Song_()
        { }
        public Song_(int id, string name)
        {
            Id = id;
            Name = name;
        }


        //might need to add a ToString() override
    }
}
